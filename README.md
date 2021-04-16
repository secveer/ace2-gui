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
* Backend documentation: http://localhost:8888/docs
* Frontend application: http://localhost:9999

### Backend (FastAPI) commands
#### Creating Alembic database revisions
When you make changes to the SQLAlchemy database models, you will need to create a new Alembic database revision. You can use the helper script to use Alembic's "autogenerate" feature to build what it thinks is the appropriate migration files:
```
bin/db-revision.sh "Your revision tag"
```

After running this command, your new database migration files will be found in `backend/app/db/migrations/versions/`. You should **always** review the migration files for accuracy before commiting them to the repository (and applying them in production). Alembic's autogenerate feature has [some limitations and caveats](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) to be aware of.

#### Applying Alembic database revisions
The revisions are automatically applied to your development environment when you use the `bin/reset-dev-container.sh` helper script. If you would like to apply them without resetting your environment, you can run:
```
bin/db-upgrade.sh
```

#### Run unit tests
```
docker-compose run backend pytest
```

### Frontend (Vue.js) commands
#### Compile and minify for production
```
docker-compose run frontend npm run build
```

#### Run unit tests
```
docker-compose run frontend npm run test:unit
```

#### Run end-to-end tests
```
docker-compose run frontend npm run test:e2e
```

#### Lint and fix files
```
docker-compose run frontend npm run lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).