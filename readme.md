# Deepscratch
This package is a personal project to implement common machine deep learning methods from scratch.

## Design choices
### 100% Jupyter
As the aim of the package is to illustrate the mathematics and implementations of the techniques, all code is implemented in  jupyter notebooks.

Such that techniques can be imported from one notebook to another (as in a traditional python package), deepscratch uses custom import hooks that intercept import statements, converting the jupyter notebooks to python scripts on-the-fly.

### Jax
Numerical operations are implemented in the jax library. jax was chosen over pytorch and tensorflow as it permits numpy-type manipulation of arrays, and so allowing clear exposition of the techniques, whilst still be sufficiently performant for deep learning.

### Small-scale Data
The aim is to enable running of models on device; with cpu-execution possible. To this end, the size of datasets is limited, for instance using [ImageNette](https://github.com/fastai/imagenette) instead of the full ImageNet. The intuition can be captured whilst making the models accessible regardless of available hardward.

## Getting started
Read through the cookbooks to see high level implementations of common architectures (MLP, CNN, RNN, etc.) on canonical datasets such as MNIST and ImageNette.