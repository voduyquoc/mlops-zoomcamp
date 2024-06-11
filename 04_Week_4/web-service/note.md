pip freeze | grep scikit-learn
pipenv shell

In VM:
pipenv install gunicorn
gunicorn --bind 0.0.0.0:9696 predict:app

In Windows:
pipenv install waitress
waitress-serve --listen=0.0.0.0:9696 predict:app

Install request package in dev environment for testing
pipenv install --dev requests


docker build -t ride-duration-prediction-service:v1 .

docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1