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

stop:
```shell script
docker-compose down
```
