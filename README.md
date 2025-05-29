# smart-store-justindavidson
Module 1 Assignment for CSIS 44632

# Module 2 Changes
Added logger script to utils folder

Added data preparation script to scripts folder

Ran the following scripts 

```shell
git pull
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel
py -m pip install --upgrade -r requirements.txt --timeout 100
py scripts/data_prep.py
```
Ran the following scripts to push changes to Github repo.

```shell
git add .
git commit -m "ran initial data_prep.py"
git push -u origin main
```
# Module 3 Changes
Added data scrubber script

Added data preparation scripts 

Added output of data preparation scripts (new csv files found in data/prepared)

# Module 4 Changes
Added a script to perform ETL processes and put the smart sales data into a datawarehouse.

Table schema was determined by taking sales data to be the facts table and using customers and product data to make dimension tables. 

Challenges encountered were improper naming of my columns, but once I got those resolved the .db file was generated with no issues. 

May have had issues with my data scrubber not fulling cleaning data either because a duplicate sales record still existed in my sales file (whoops).

Below are screenshots of my smart_sales.db tables:

![Customer Data Screenshot](/data/dw/customer%20data.JPG?raw=true)

![Product Data Screenshot](/data/dw/product%20data.JPG?raw=true)

![Sale Data Screenshot](/data/dw/sale%20data.JPG?raw=true)

It's cool being able to add screenshots to markdown files.