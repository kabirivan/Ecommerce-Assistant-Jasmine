# Ecommerce-Assistant

## Setup

### Python setup
Currently this projects just work using **python 3.7** so It is recommend that make sure you have this python version. To check run on command line:
```
python3 --version
```

If you do not have the correct version, please download it from [here](http:/https://www.python.org/downloads// "here")


### Poetry Installation
You can follow the steps [here](https://python-poetry.org/docs/#installation "here") to intall poetry in either osx / linux or windows.


### Spacy configuration
Run this command to download the espanish spacy model for entity extraction

```
poetry run python -m spacy download es_core_news_md
```


### Installation
The following commands helps to install python packages needed to make this project run correctly locally.
```
git clone https://github.com/kabirivan/Ecommerce-Assistant.git
cd Ecommerce-Assistant
```

#### Package setup using poetry
```
poetry shell
poetry install
rasa train
```
## Development

### Activate ngrok to serve on https
In order to make this example to test, please use ngrok. You can setup ngrok in you pc from [here](https://ngrok.com/ "here").

Run on console the following command. It will expose 5005 local port on internet.
```
./ngrok http 5005
```

### Start project
Start action server and Duckling

```
docker-compose -f docker-compose-dev.yml up
```

Run on console the following command. It will start project on port 5005
```
poetry shell
rasa shell
rasa run --enable-api --cors "*"
rasa interactive
```

## Production
```
docker-compose up
```

## Extras
- [Rasa API](https://rasa.com/docs/rasa/pages/http-apihttp:// "Rasa API")
- [Poetry Manager](https://hackersandslackers.com/python-poetry-package-manager/ "Poetry Manager")
- [Poetry doc](https://python-poetry.org/docs/cli/ "Poetry doc")


#### Remove Env
```
poetry env info
poetry env remove 3.7
rm -rf `poetry env info -p`
```
#### Remove Credentials
```
git rm --cached credentials.yml
```
