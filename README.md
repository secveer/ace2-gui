# ACE2 GUI
The ACE2 GUI is comprised of three main components: a PostgreSQL database, a FastAPI backend, and a Vue.js frontend.

## Project setup for development
The included `docker-compose.yml` file runs the full application in development mode. This uses volumes to your local source code directories and enables hot-reload for the Vue.js and FastAPI applications.
```
docker-compose build
docker-compose up
```

Once the development environment is built and started, you can access the components:

* Backend test endpoint: http://localhost:8888/ping
* Backend documentation: http://localhost:8888/docs
* Frontend application: http://localhost:9999

## Backend (FastAPI) commands
### Run unit tests
```
docker-compose run backend pytest
```

## Frontend (Vue.js) commands
### Compile and minify for production
```
docker-compose run frontend npm run build
```

### Run unit tests
```
docker-compose run frontend npm run test:unit
```

### Run end-to-end tests
```
docker-compose run frontend npm run test:e2e
```

### Lint and fix files
```
docker-compose run frontend npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).