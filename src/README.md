# RUN Docker

### Docker need to be ran from top of the dir tree
```bash
#start docker database (db) and backed services 
docker-compose up -d 
```

# Application

Base url is `http://127.0.0.1:8000`

### Valid endpoints (Swagger API)

`http://127.0.0.1:8000/docs`


# STOP Docker
```bash
#stop both services and delete volumes (database do not preserve)
docker-compose down
```


