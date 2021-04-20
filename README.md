# ACE2 GUI
The ACE2 GUI is comprised of three main components: a PostgreSQL database, a FastAPI backend, and a Vue.js frontend.

## Project setup for development
The included `docker-compose-dev.yml` file runs the full application in development mode. This uses volumes to your local source code directories and enables hot-reload for the Vue.js and FastAPI applications. There are various scripts included to simplify some of the docker-compose commands.

To rebuild the development environment (which will also erase your development database):
```
bin/reset-dev-container.sh
```

This script will generate random passwords for the database user as well as the pgAdmin user. If you need to access either of these, you can view them in the `db/.env` file, which configures the environment variables that will be loaded into the database container.

Once the development environment is built and started, you can access the components:

* Database pgAdmin GUI: http://localhost:7777
* Backend API documentation: http://localhost:8888/docs
* Frontend application: http://localhost:9999