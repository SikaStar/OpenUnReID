## Model Zoo

**Note:**
- All the models are selected by the performance on validation sets.
- We adopt the same training settings (found in config files) on all datasets for convenience. Performance can be further boosted by tuning hyper-parameters on specific datasets. We will add more comparisons.
- USL methods are trained without any labeled data, and UDA methods are all trained in a semi-supervised manner with domain-specific BatchNorms.
- The pipeline of `UDA_TP` has been improved to achieve much better performance than its original paper. We will add technical details in [UDA_TP/README.md](../tools/UDA_TP).

### Unsupervised learning (USL) on object re-ID

- `Direct infer` models are directly tested on the re-ID datasets with ImageNet pre-trained weights.
<!-- - Methods (`UDA_TP`, `MMT`, `SpCL`, etc.) are in the USL version without any labeled data. -->

#### DukeMTMC-reID

| Method | Backbone | Pre-trained | mAP(%) | top-1(%) | top-5(%) | top-10(%) | Train time | Download |
| ----- | :------: | :---------: | :----: | :------: | :------: | :-------: | :------: | :------: |
| Direct infer | ResNet50 | ImageNet | 2.3 | 7.5 | 14.7 | 18.1 | n/a |
| [UDA_TP](../tools/UDA_TP) | ResNet50 | ImageNet | 54.7 | 72.9 | 83.5 | 87.2 | ~2.5h | [[drive]](https://drive.google.com/file/d/1zY8VBIq0QifuljX_WK51xDY6ATZaVjEm/view?usp=sharing) |
| [MMT](../tools/MMT/) | ResNet50 | ImageNet | 57.0 | 71.7 | 84.1 | 88.6 | ~4h | [[drive]](https://drive.google.com/file/d/1DnQAFnYowHq6lsX6dcAZqDhsnbd52MyK/view?usp=sharing) |
| [SpCL](../tools/SpCL/) | ResNet50 | ImageNet | 67.1 | 82.4 | 90.8 | 93.0 | ~2h | [[drive]](https://drive.google.com/file/d/16BpSqexmHtWg293X5oZRrBWxVfSdgER9/view?usp=sharing) |

#### Market-1501

| Method | Backbone | Pre-trained | mAP(%) | top-1(%) | top-5(%) | top-10(%) | Train time | Download |
| ----- | :------: | :---------: | :----: | :------: | :------: | :-------: | :------: | :------: |
| Direct infer | ResNet50 | ImageNet | 2.2 | 6.7 | 14.9 | 20.1 | n/a |
| [UDA_TP](../tools/UDA_TP) | ResNet50 | ImageNet | 70.5 | 87.9 | 95.7 | 97.1 | ~2.5h | [[drive]](https://drive.google.com/file/d/1Q3NABjVKDmzIlPMliyRneQeOxPg6k-tG/view?usp=sharing) |
| [MMT](../tools/MMT/) | ResNet50 | ImageNet | 71.0 | 86.9 | 95.0 | 97.1 | ~4h | [[drive]](https://drive.google.com/file/d/1fio3UkTXzhm8WDTAYvFdnm5SSrbSlWqX/view?usp=sharing) |
| [SpCL](../tools/SpCL/) | ResNet50 | ImageNet | 76.0 | 89.5 | 96.2 | 97.5 | ~2h | [[drive]](https://drive.google.com/file/d/1cBfDcZGAdL1x7u53Wkci2xZBQ6A-uW7a/view?usp=sharing) |

#### ... (TBD)


### Unsupervised domain adaptation (UDA) on object re-ID

- `Direct infer` models are trained on the source-domain datasets ([source_pretrain](../tools/source_pretrain)) and directly tested on the target-domain datasets.
- UDA methods (`UDA_TP`, `MMT`, `SpCL`, etc.) starting from ImageNet means that they are trained end-to-end in only one stage without source-domain pre-training.
<!-- - Domain-specific BNs are adopted in all UDA methods. -->

#### Market-1501 -> DukeMTMC-reID

| Method | Backbone | Pre-trained | mAP(%) | top-1(%) | top-5(%) | top-10(%) | Train time | Download |
| ----- | :------: | :---------: | :----: | :------: | :------: | :-------: | :------: | :------: |
| Direct infer | ResNet50 | Market-1501 | 28.1 | 49.3 | 64.3 | 69.7 | ~1h | [[drive]](https://drive.google.com/file/d/1kEVGJfzmGdRM6EYk9Pigs26df2Xk15Dg/view?usp=sharing) |
| [UDA_TP](../tools/UDA_TP) | ResNet50 | ImageNet | 60.4 | 75.9 | 86.2 | 89.8 | ~3h | [[drive]](https://drive.google.com/file/d/1z14TQ1Jc4nlFQMAqULxtRbcyGKNY2Jlt/view?usp=sharing) |
| [MMT](../tools/MMT/) | ResNet50 | ImageNet | 67.7 | 80.3 | 89.9 | 92.9 | ~6h | [[drive]](https://drive.google.com/file/d/1gXuVxSS9gKuGVPa76OBIB7WGdmAdqA7n/view?usp=sharing) |
| [SpCL](../tools/SpCL/) | ResNet50 | ImageNet | 70.4 | 83.8 | 91.2 | 93.4 | ~3h | [[drive]](https://drive.google.com/file/d/110W6Rvp0gylF8WNKTRrgVteIvA5qCtYQ/view?usp=sharing) |
<!-- | [SDA](../tools/SDA/) | ResNet50 | Market-1501 | -->

#### DukeMTMC-reID -> Market-1501

| Method | Backbone | Pre-trained | mAP(%) | top-1(%) | top-5(%) | top-10(%) | Train time | Download |
| ----- | :------: | :---------: | :----: | :------: | :------: | :-------: | :------: | :------: |
| Direct infer | ResNet50 | DukeMTMC-reID | 27.2 | 58.9 | 75.7 | 81.4 | ~1h | [[drive]](https://drive.google.com/file/d/1fIQduTzMHtZ_LTPzburtlaKu7aljYjRx/view?usp=sharing) |
| [UDA_TP](../tools/UDA_TP) | ResNet50 | ImageNet | 75.6 | 90.9 | 96.6 | 97.8 | ~3h | [[drive]](https://drive.google.com/file/d/1gDFSI64Wqln19FG8XRRvOd0pebmvqb-V/view?usp=sharing) |
| [MMT](../tools/MMT/) | ResNet50 | ImageNet | 80.9 | 92.2 | 97.6 | 98.4 | ~6h | [[drive]](https://drive.google.com/file/d/1fOljN4B3XJbfyt1CZoDy1A08MlhcQQ8M/view?usp=sharing) |
| [SpCL](../tools/SpCL/) | ResNet50 | ImageNet | 78.2 | 90.5 | 96.6 | 97.8 | ~3h | [[drive]](https://drive.google.com/file/d/1SUgk6oerpA-AZf2Z30Mww_S3DUPpBnpT/view?usp=sharing) |
<!-- | [SDA](../tools/SDA/) | ResNet50 | DukeMTMC-reID | -->

#### ... (TBD)
