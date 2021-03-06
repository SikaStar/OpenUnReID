import os
import os.path as osp
import sys
import copy
import argparse
import time
import shutil
import warnings
from datetime import timedelta
from pathlib import Path
import torch

from openunreid.apis import test_reid, BaseRunner
from openunreid.models import build_model
from openunreid.models.losses import build_loss
from openunreid.data import build_train_dataloader, build_test_dataloader
from openunreid.core.solvers import build_optimizer, build_lr_scheduler
from openunreid.utils.config import cfg, cfg_from_yaml_file, cfg_from_list, log_config_to_file
from openunreid.utils.dist_utils import init_dist, synchronize
from openunreid.utils.logger import Logger
from openunreid.utils.file_utils import mkdir_if_missing


def parge_config():
    parser = argparse.ArgumentParser(description='Pretraining on source-domain datasets')
    parser.add_argument('config', help='train config file path')
    parser.add_argument('--work-dir', help='the dir to save logs and models', default='')
    parser.add_argument('--resume-from', help='the checkpoint file to resume from')
    parser.add_argument('--launcher', type=str,
                        choices=['none', 'pytorch', 'slurm'],
                        default='none', help='job launcher')
    parser.add_argument('--tcp-port', type=str, default='5017')
    parser.add_argument('--set', dest='set_cfgs', default=None,
                        nargs=argparse.REMAINDER,
                        help='set extra config keys if needed')
    args = parser.parse_args()

    cfg_from_yaml_file(args.config, cfg)
    cfg.launcher = args.launcher
    cfg.tcp_port = args.tcp_port
    if not args.work_dir:
        args.work_dir = Path(args.config).stem
    cfg.work_dir = cfg.LOGS_ROOT / args.work_dir
    mkdir_if_missing(cfg.work_dir)
    if args.set_cfgs is not None:
        cfg_from_list(args.set_cfgs, cfg)

    shutil.copy(args.config, cfg.work_dir / 'config.yaml')

    return args, cfg


def main():
    start_time = time.monotonic()

    # init distributed training
    args, cfg = parge_config()
    dist = init_dist(cfg)
    synchronize()

    # init logging file
    logger = Logger(cfg.work_dir / 'log.txt')
    sys.stdout = logger
    print("==========\nArgs:{}\n==========".format(args))
    log_config_to_file(cfg)

    # build train loader
    train_loader, _ = build_train_dataloader(cfg)

    # build model
    model = build_model(
                cfg,
                train_loader.loader.dataset.num_pids
            )
    model.cuda()

    if dist:
        model = torch.nn.parallel.DistributedDataParallel(
                    model,
                    device_ids=[cfg.gpu],
                    output_device=cfg.gpu,
                    find_unused_parameters=True,
                )
    elif (cfg.total_gpus>1):
        model = torch.nn.DataParallel(model)

    # build optimizer
    optimizer = build_optimizer([model], **cfg.TRAIN.OPTIM)

    # build lr_scheduler
    if cfg.TRAIN.SCHEDULER.lr_scheduler is not None:
        lr_scheduler = build_lr_scheduler(optimizer, **cfg.TRAIN.SCHEDULER)
    else:
        lr_scheduler = None

    # build loss functions
    criterions = build_loss(cfg.TRAIN,
            num_classes=train_loader.loader.dataset.num_pids, cuda=True)

    # build runner
    runner = BaseRunner(
                cfg,
                model,
                optimizer,
                criterions,
                train_loader,
                lr_scheduler = lr_scheduler
            )

    # resume
    if args.resume_from:
        runner.resume(args.resume_from)

    # start training
    runner.run()

    # load the best model
    runner.resume(cfg.work_dir / 'model_best.pth')

    # final testing
    test_loaders, queries, galleries = build_test_dataloader(cfg)
    for i, (loader, query, gallery) in enumerate(zip(test_loaders, queries, galleries)):
        cmc, mAP = test_reid(
                        cfg,
                        model,
                        loader,
                        query,
                        gallery,
                        dataset_name = cfg.TEST.datasets[i]
                    )

    # print time
    end_time = time.monotonic()
    print('Total running time: ',
        timedelta(seconds=end_time - start_time))


if __name__ == '__main__':
    main()
