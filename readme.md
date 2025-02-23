# Deepscratch
This package is a personal project to implement common machine deep learning methods from scratch.

## Design choices
### 100% Jupyter
As the aim of the package is to illustrate the mathematics and implementations of the techniques, all code is implemented in  jupyter notebooks.

Such that techniques can be imported from one notebook to another (as in a traditional python package), deepscratch uses custom import hooks that intercept import statements, converting the jupyter notebooks to python scripts on-the-fly.

## Jax
Numerical operations are implemented in the jax library. jax was chosen over pytorch and tensorflow as it permits numpy-type manipulation of arrays, and so allowing clear exposition of the techniques, whilst still be sufficiently performant for deep learning.