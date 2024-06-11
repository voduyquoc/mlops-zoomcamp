cp ../web-service-mlflow/random-forest.ipynb score.ipynb

jupyter nbconvert --to script score.ipynb

rm output/green/*

python score.py green 2021 4 RUN_ID

