# SPICS: An Unsupervised Framework for Analysingthe Spatiotemporal Evolution of Industry Clusters 

#### This repo contains the Python implementation of the paper SPICS: An Unsupervised Framework for Analysingthe Spatiotemporal Evolution of Industry Clusters in IJOC (Software Tool)

## Requirements

#### The codes have been tested with the following packages:
* Python 3.6
* Gensim
* pandas

## Quick Demo

#### To run the model (including data processing), clone the repo and decompress the demo data archive by executing the following commands:

``` 
git clone git@github.com:jeaninesong/SPICS.git
cd LDA
python LDA.py --f input_file
```

##### You can use --rf to change the name of output file, --clusterNum to change the number of clusters, and --keywordsNum to change the number of keywords in each cluster. 

#### To run the evaluation:

``` 
cd Evaluation
python evaluation.py --sec 1 --rf LDA_output_file
``` 
##### --sec 1 is for the evaluation of section level in SIC code, --sec 0 is for the division level in SIC code. 


#### To use the powerbi software:

#### You can open the Powerbi file. The SPICS.pbix is the powerbi report and there is a user manual (.pdf) for detailed guidance. 

## Citation

#### If you find the paper or the implementation helpful, please cite the following paper: