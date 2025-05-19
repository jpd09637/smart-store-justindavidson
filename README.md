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
