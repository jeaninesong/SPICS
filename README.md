# SPICS: An Unsupervised Framework for Analysingthe Spatiotemporal Evolution of Industry Clusters 

#### This repo contains the Python implementation of the paper SPICS: An Unsupervised Framework for Analysingthe Spatiotemporal Evolution of Industry Clusters in INFORMS (Software Tool)

## Requirements

#### The codes have been tested with the following packages:
* Python 3.6
* Gensim
* pandas

## Quick Demo

#### To run the model, clone the repo and decompress the demo data archive by executing the following commands:

``` 
git clone git@github.com:jeaninesong/SPICS.git
cd LDA
python LDA.py --f input_file
```

#### To run the evaluation:

``` 
cd Evaluation
python evaluation.py --sec 1 --rf LDA_output_file
``` 

## Citation

#### If you find the paper or the implementation helpful, please cite the following paper: