#!/usr/bin/env python3

# This script initializes the Docker development environment by creating
# random passwords for the database user and creating the .env files so that
# the containers have the appropriate environment variables set.

import random
import string


def generate_password(min_length: int = 23, max_length: int = 32) -> str:
    return "".join(random.choices(string.ascii_letters, k=random.randint(min_length, max_length)))


def main():
    # Set up the environment variables that are needed for the application
    database_hostname = "db"
    database_port = 5432
    database_db = "ace"
    database_user = "ace"
    database_password = generate_password()
    database_admin_email = "ace@ace.com"
    database_admin_password = generate_password()
    database_url = f"postgresql://{database_user}:{database_password}@{database_hostname}:{database_port}/{database_db}"

    # Write the database .env file
    with open("db/.env", "w") as f:
        text = f"""POSTGRES_DB={database_db}
POSTGRES_USER={database_user}
POSTGRES_PASSWORD={database_password}
PGADMIN_DEFAULT_EMAIL={database_admin_email}
PGADMIN_DEFAULT_PASSWORD={database_admin_password}"""
        f.write(text)

    # Write the backend .env file
    with open("backend/.env", "w") as f:
        text = f"""DATABASE_URL={database_url}
ACE_DEV=true"""
        f.write(text)


if __name__ == "__main__":
    main()
