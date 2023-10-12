# Refactoring Project

This repository contains the first project from the neuefische MLE bootcamp.

## Setup

To setup the environment you can use the [requirements.txt](./requirements.txt) file.
You can install it with the following commands:

```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Project overview

The aim of this project was to refactor the python code from a jupyter notebook into python files in order to build a pipeline for data cleaning and feature engineering. Afterwards a FastAPI for creating, updating and deleting houses should be build.

### Refactoring

The original code can be found in the [King-County.ipynb](./King-County.ipynb) notebook. In a first iteration the necessary code was transferred to the [data_cleaning_functions.py](./scripts/data_cleaning_functions.py) file in the scripts folder and refactored into python functions. In a next step those cleaning and pre-processing functions were rewritten into custom transformer classes which can be seamlessly integrated into a scikit-learn pipeline ([preprocessing.py](./scripts/preprocessing.py)). The last python file [pipeline.py](./scripts/pipeline.py) contains the full pre-processing pipeline starting with importing the raw data, setting up a pre-processing pipeline with standard transformers from sk-learn as well as the custom transformers from the [preprocessing.py](./scripts/preprocessing.py) script. After applying the pipeline to the data set it is saved as a pandas DataFrame and exported as a .csv file. In order to keep the updating of the houses via the API simple, only 5 features were kept after pre-processing.


### API 

The [API](./API/) folder contains the necessary files for the CRUD FastAPI. 

In the [schemas.py](./API/schemas.py) file the Pydantic model for the data is defined. The [models.py](./API/models.py) file contains the definition of the database models. [database.py](./API/database.py) contains the code to connect to the database. And finally, the [main.py](./API/main.py) file contains the code for the actual FastAPI. 

You can run the FastAPI app on port 8000 with: 

```Bash
uvicorn main:app --reload --port 8000
```

In order to add a new house run:

```Bash
curl -X 'POST' \
'http://localhost:8000/houses' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
"id": 20, 
"price": 50000, 
"bedrooms": 2, 
"center_distance": 1.5, 
"last_known_change": 1998
}'
```

In order to retrieve the houses in the database run:

```Bash
curl -X 'GET' 'http://localhost:8000/houses' -H 'accept: application/json'
```

### Docker

In order to run the API in a docker container the [docker-compose.yml](./docker-compose.yml) file and the [Dockerfile](./API/Dockerfile) file contain the necessary configurations. The connection details for the database should be stored in a `.env` file. Make sure that the database connection string is defined like this:

```
DOCKER_DB_CONN='postgresql://postgres:postgres@postgres_compose:5432/<db-name>'
```

Start and stop the container with:

```Bash
docker compose up -d
docker compose down
```