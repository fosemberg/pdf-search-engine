# PDF search engine

## Set up

To connect to Yandex.Cloud:
- Create `.env` file in the `pse` directory
- Define the following env variables:
```
IAM_TOKEN=<Yandex.Cloud IAM token>
FOLDER_ID=<ID of folder in Yandex.Cloud>
```

## Deploy

start:
```shell script
docker-compose up
```

django:
```shell script
$ docker exec -it web /bin/bash
$ cd pse
$ python manage.py populatedb                           # to insert test data to db
$ python manage.py get_document --name <document_name>  # to get document from db by name
```

stop:
```shell script
docker-compose down
```

## Search

To search use `http://0.0.0.0:8000/fast-search/` or `http://0.0.0.0:8000/slow-search/`

with body
`{
	"name":"NUP4114",
	"keywords":["voltage", "current", "test"]
}`