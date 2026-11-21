# One Model is All You Need: Multi-Task Learning Enables Simultaneous Histology Image Segmentation and Classification

## Run the CPU replay

Install Docker and obtain the Cerberus model weights from the upstream project. Keep
`weights.tar` outside the checkout. The example below mounts it read-only. The image
does not include weights. [Upstream model weights](https://warwick.ac.uk/fac/cross_fac/tia/software/cerberus/)

```sh
docker build -t cerberus-replay .
WEIGHTS="$(realpath /path/to/weights.tar)"
docker run --name cerberus-replay --cpus=4 --memory=8g \
  --mount "type=bind,source=$WEIGHTS,target=/workdir/resnet34_cerberus/weights.tar,readonly" \
  cerberus-replay
docker cp cerberus-replay:/workdir/output_test/overlay ./output_test
```

The container fetches a fixed Cerberus revision and applies the CPU patch. It runs
inference on the two sample images and compares the decoded overlay pixels against
the saved references. Fetch, patch, inference and image comparison errors return a
nonzero exit status. On macOS, allocate enough Docker CPU and memory for the run.

## Test the comparison

The pixel checks use Pillow and small local fixtures.

```sh
python -m unittest discover -s tests
```

## References

[Page](https://paperswithcode.com/paper/one-model-is-all-you-need-multi-task-learning) on __Papers With Code__

__Cerberus__ [repository](https://github.com/TissueImageAnalytics/cerberus#one-model-is-all-you-need-multi-task-learning-enables-simultaneous-histology-image-segmentation-and-classification)

Download the weights by visiting [this page](https://warwick.ac.uk/fac/cross_fac/tia/software/cerberus/), also for more information about the project

Test datasets
- Gland Segmentation in Histology Images Challenge — [GlaS Dataset](https://academictorrents.com/details/208814dd113c2b0a242e74e832ccac28fcff74e5)
- Dataset provided by Cerberus developers on [this page](https://warwick.ac.uk/fac/cross_fac/tia/software/cerberus/)

## Citation

```
@article{graham2022one,
  title={One model is all you need: multi-task learning enables simultaneous histology image segmentation and classification},
  author={Graham, Simon and Vu, Quoc Dang and Jahanifar, Mostafa and Raza, Shan E Ahmed and Minhas, Fayyaz and Snead, David and Rajpoot, Nasir},
  journal={Medical Image Analysis},
  pages={102685},
  year={2022},
  publisher={Elsevier}
}
```
