# Written by Yixiao Ge

import torch
import torch.nn as nn

from .classification import *
from .triplet import *
from .memory import HybridMemory


def build_loss(
    cfg,
    num_classes=None,
    num_features=None,
    num_memory=None,
    cuda=False
):

    criterions = {}
    for loss_name in cfg.losses.keys():

        if (loss_name=='cross_entropy'):
            assert (num_classes is not None)
            criterions['cross_entropy'] = CrossEntropyLoss(num_classes)

        elif (loss_name=='soft_entropy'):
            criterions['soft_entropy'] = SoftEntropyLoss()

        elif (loss_name=='triplet'):
            if ('margin' not in cfg): cfg.triplet.margin = 0.3
            criterions['triplet'] = TripletLoss(margin=cfg.margin)

        elif (loss_name=='softmax_triplet'):
            if ('margin' not in cfg): cfg.triplet.margin = 0.
            criterions['softmax_triplet'] = SoftmaxTripletLoss(margin=cfg.triplet.margin)

        elif (loss_name=='soft_softmax_triplet'):
            criterions['soft_softmax_triplet'] = SoftSoftmaxTripletLoss()

        elif (loss_name=='hybrid_memory'):
            assert (num_features is not None and num_memory is not None)
            if ('temp' not in cfg): cfg.memory.temp = 0.05
            if ('momentum' not in cfg): cfg.memory.momentum = 0.2
            criterions['hybrid_memory'] = HybridMemory(num_features, num_memory,
                                            temp=cfg.memory.temp, momentum=cfg.memory.momentum)

        else:
            raise KeyError("Unknown loss:", loss_name)

    if cuda:
        for loss in criterions.values():
            loss.cuda()

    return criterions
