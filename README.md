# Ecommerce-Assistant-Jasmine


#### Remove Env
poetry env info
poetry env remove 3.7
rm -rf `poetry env info -p`

#### Remove Credentials
git rm --cached credentials.yml

### Run Rasa
rasa run --enable-api --cors "*"


docker-compose -f docker-compose-dev.yml up