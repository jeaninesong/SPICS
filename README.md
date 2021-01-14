# Industry Classifcation Tool

Resource for industry classification IJOC submission

# SPICS: An Unsupervised Framework for Analysing the Spatiotemporal Evolution of Industry Clusters 

This repo contains the Python implementation of the paper SPICS: An Unsupervised Framework for Analysing the Spatiotemporal Evolution of Industry Clusters in IJOC (Software Tool)

## Requirements

#### The codes have been tested with the following packages:
* Python 3.6
* Gensim
* spaCy
* pandas


## Input data and Power BI file 

You can download the whole input data (.csv) and Power BI file (.pbix) with the following links:

#### Google Drive:

```
https://drive.google.com/drive/folders/1SyTS4Gt_0IIF60-_LTZ0HdpbVGlI6DRH?usp=sharing
```
#### One Drive
```
https://mylingnan-my.sharepoint.com/:f:/g/personal/allentan_ln_edu_hk/Ek-O_ydpy-xApwg5bxE-ZKgBDQzzkFBTUh25b4ya7tciPg?e=k1qYKh
```

Also, we provide a toy raw data (demo_data_IREC.csv and demo_data_WALMID.csv) for you to test the whole pipeline in the data file.

## Demo

To run the model (including data processing), clone this repo and copy the demo data (data/demo_data_IREC.csv or data/demo_data_WALMID.csv) into src/LDA file archive by executing the following commands:

``` 
git clone git@github.com:ludsl/Industry_classifcation_tool.git
cd src/LDA
python LDA.py --f demo_data_IREC.csv --rf LDA_irec_output
```

You can use --rf to change the name of output file, --clusterNum to change the number of clusters, and --keywordsNum to change the number of keywords in each cluster. 

### To calculate the location quotient:
Copy the LDA output of both IREC and WALMID (LDA/IREC_LDA_output.csv and LDA/WALMID_LDA_output.csv) into scr/LQ file archive by executing the following commands:

```
cd src/LQ
python location_quotient.py --irec IREC_LDA_output.csv --walmidf WALMID_LDA_output.csv
```

### To run the evaluation:

Copy the LDA output data (LDA/LDA_output.csv) into src/Evaluation file archive by executing the following commands:

``` 
cd src/Evaluation
python evaluation.py --sec 1 --rf LDA_output
``` 
--sec 1 is for the evaluation of section level in SIC code, --sec 0 is for the division level in SIC code. 

### To use the Power BI software:

You can download and open the .pbix file in the above links to use the Power BI software.

You can copy the LDA output of both IREC and WALMID to src/PowerBI, and the output of location quotient (location_quotient.xlsx) and then use to src/PowerBI/powerbi.py to generate the input data for the Power BI software by executing the following commands:

```
cd src/PowerBI/powerbi.py
python powerbi.py --irecf LDA_output_IREC.csv --walmidf LDA_output_WALMID.csv
```

There is a user manual (docs/Manual_of_Power_BI.pdf) for detailed guidance to generate Power BI software. 


