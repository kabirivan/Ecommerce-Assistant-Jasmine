<p align="center"> 
  <img src="images/logo.png" alt="Jasmine Logo" width="80px" height="80px">
</p>
<h1 align="center"> Jasmine Assistant </h1>
<h3 align="center"> Rasa Open Source | Algolia | Airtable | Rasa X </h3>
<h5 align="center"> Thesis project - <a href="https://www.epn.edu.ec/">Escuela Politécnica Nacional</a> (June 2022) </h5>

<p align="center"> 
  <img src="images/assistant.png" alt="Assistant Views" height="582px">
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project"> ✏️ About The Project</h2>

<p align="justify"> 
  In this work, a conversational assistant capable of accompanying the client throughout the clothing discovery process was developed, through Rasa; a framework that combines the comprehension and processing of natural language based on transformer-type neural networks allowing to improve the effectiveness of responses.
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- RESULTS -->
<h2 id="results"> 📓 Results</h2>

<p align="justify"> 
  The results of this work showed that through Rasa it is possible to create assistants as personalized as desired and that incorporating continuous training and evaluation processes with real users makes it possible for the model to be generalized to real-world scenarios, thus increasing the rate effectiveness.
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- PROJECT FILES DESCRIPTION -->
<h2 id="assistant-skills"> 📌 NLU Pipeline</h2>

<ul>
  <li><b>Tokenizers</b> - WhiteSpaceTokenizer</li>
  <li><b>(1) Feature Extractor</b> - RegexFeaturizer</li>
  <li><b>(2) Feature Extractor</b> - LexicalSyntacticFeaturizer</li>
  <li><b>(3) Feature Extractor</b> - CountVectorsFeaturizer</li>
  <li><b>(1) Intent Classifier</b> - DIETClassifier</li>
  <li><b>(2) Intent Classifier</b> - FallbackClassifier</li>
  <li><b>(1) Entity Extractor</b> - DIETClassifier</li>
  <li><b>(2) Entity Extractor</b> - EntitySynonymMapper</li>
  <li><b>(3) Entity Extractor</b> - DucklingEntityExtractor</li>
  <li><b>(4) Entity Extractor</b> - SpacyEntityExtractor</li>
</ul>


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
