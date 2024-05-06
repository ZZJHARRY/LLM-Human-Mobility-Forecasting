# ***L***arge ***L***anguage ***M***odels for ***H***uman ***M***obility ***F***orecasting (LLM-HMF)

### Introduction

LLM-HMF is an LLM-powered end-to-end human mobility forecasting framework.

### Data

There are currently two processed datasets in this repository:

1. geolife - [GNSS tracking dataset- Geolife](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=24ccdcba118ff9a72de4840efb848c7c852ef247)
2. fsq - [Foursquare New York City (FSQ-NYC)](https://ieeexplore.ieee.org/abstract/document/6844862/?casa_token=8_aUlbQkmzEAAAAA:ALnRKLPqIFPKNZtA7j2cTpZEYG00g7ZSzAY1kTg_X6WNLwI55jhYrZ5Lwh5vx8zjMFledj1KvGE)

The data is hosted in `/data`. The data preprocessing steps are following [Context-aware multi-head self-attentional neural network model for next location prediction](https://arxiv.org/abs/2212.01953). All the data files are generated from the data preprocessing scripts available [here](https://github.com/mie-lab/location-prediction).

### Run the LLM-HMF Model

#### 1. Get an OpenAI account
If you already have an account and have set up API keys, skip this step. Otherwise, go to [OpenAI API website](https://openai.com/blog/openai-api) and sign up. Once you have an account, create an API key [here](https://platform.openai.com/account/api-keys). You may also need to set up your payment [here](https://platform.openai.com/account/billing/overview) in order to use the API.

#### 2. Run the scripts to start the prediction process.
Specify your OpenAI API Key in the beginning of the script `main.py`, change the parameters in the main function if necessary and start the prediction process by simply running the following scripts:

```bash
$ pip install -r requirements.txt
$ python main.py
```
The log file will be stored in `/logs` and prediction results will be stored in `/output`.

### Code Structure

```
.
|   README.md
|   main.py
|   requirements.txt
|   metrics.ipynb
|   LICENSE
|   
+---core
|   |
|   +---llm_model
|   |       model.py
|   |
|   +---prompt
|   |       constructor.py
|   |       content.py
|   |
|   \---query
|           constructor.py
|           content.py
|
+---utils
|   |   dataset_preparation.py
|   |   helper.py
|   |
|   +---llm_model
|   |       model.py
|   |
|   +---prompt
|   |       constructor.py
|   |       content.py
|   |
|   \---query
|           constructor.py
|           content.py
|
+---data
|   |
|   +---fsq
|   |       foursquare_test.csv
|   |       foursquare_testset.pk
|   |       foursquare_train.csv
|   |       foursquare_valid.csv
|   |       random_id_subset.pkl
|   |       tv_data.csv
|   |
|   \---geolife
|           geolife_test.csv
|           geolife_testset.pk
|           geolife_train.csv
|           geolife_valid.csv
|           tv_data.csv
|           
+---output
|   |   
|   \---geolife
|           |
|           \---top10_wot
|
+---logs
|   |   
|   +---fsq
|   |
|   \---geolife
|           
|          
\---results
    |
    +---fsq
    |
    \---geolife
            
```

### Results and evaluation
Sample prediction results (Geolife dataset) are shown in `/results`. 
To calculate the evaluation metrics, check the IPython notebook `metrics.ipynb` and run the scripts therein.

### Reference
LLM-HMF is an updated version of [LLM-Mob](https://github.com/xlwang233/LLM-Mob/tree/main) with upgraded modularization, lower cost to maintain, and stronger extensibility to more use cases.