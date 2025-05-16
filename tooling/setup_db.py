#!.venv/bin/python
"""
examples:
    setup_db.py -u user -q -t user:password:db_name

required:
    psycopg
"""

import argparse
import getpass
import os
import sys
from dataclasses import dataclass
from typing import Self

import psycopg
from psycopg.errors import DuplicateDatabase, DuplicateObject


@dataclass
class DatabaseConfig:
    username: str
    database: str
    password: str

    @classmethod
    def from_str(cls, value: str) -> Self:
        try:
            username, password, database = value.split(":")
        except ValueError as err:
            msg = f"Invalid database config format. Expected 'username:password:db_name' but got {value}"  # fmt: skip
            raise argparse.ArgumentTypeError(msg) from err
        return cls(username, database, password)


def database_setup(config: DatabaseConfig, connection_url: str):
    SQL_CREATE_DB = f"CREATE DATABASE {config.database};"  # fmt: skip
    SQL_CREATE_USER = f"CREATE USER {config.username} WITH PASSWORD '{config.password}';"  # fmt: skip
    SQL_GRANT_PRIVILEGES = f"GRANT ALL PRIVILEGES ON DATABASE {config.database} TO {config.username};"  # fmt: skip
    # SQL_GRANT_SCHEMA_PRIVILEGES = f"GRANT ALL ON SCHEMA public TO {config.username};"  # fmt: skip
    SQL_ALTER_OWNER = f"ALTER DATABASE {config.database} OWNER TO {config.username};"  # fmt: skip

    def _autocommit_exec(conn, sql: str):
        conn.autocommit = True
        try:
            conn.execute(sql)
        except (DuplicateDatabase, DuplicateObject) as e:
            print(f"DUPLICATION: {e}.")
        except psycopg.errors.OperationalError as e:
            print(f"Error: {e}, exit with code 1")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)

    with psycopg.connect(connection_url) as conn:
        _autocommit_exec(conn, SQL_CREATE_USER)
        _autocommit_exec(conn, SQL_CREATE_DB)

    db_url = f"{connection_url}{config.database}"
    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(SQL_GRANT_PRIVILEGES)
                # cur.execute(SQL_GRANT_SCHEMA_PRIVILEGES)
                cur.execute(SQL_ALTER_OWNER)
    except psycopg.errors.OperationalError as e:
        print(f"Error: {e}, exit with code 1")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-url",
        type=str,
        default="localhost:5432",
        help="address:port [default: localhost:5432]",
    )
    parser.add_argument(
        "-u",
        "--username",
        default="postgres",
        help='username for connection or take value from TOOLS_POSTGRES_USER [default: "postgres"]',
    )
    parser.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help='ignore password input and take "postgres" value or from TOOLS_POSTGRES_PASSWORD [default: False]',
    )
    parser.add_argument(
        "--target",
        type=DatabaseConfig.from_str,
        help='config for target db: [example: "username:password:database"] ',
    )
    return parser


def main():
    args = get_parser().parse_args()

    privileged_user_name = args.username or os.getenv("TOOLS_POSTGRES_USER", "postgres")
    privileged_user_pass = os.getenv("TOOLS_POSTGRES_PASSWORD", "postgres")

    if not args.quite:
        privileged_user_pass = getpass.getpass() or privileged_user_pass

    connect_url = f"postgresql://{privileged_user_name}:{privileged_user_pass}@{args.url}/"
    target_database_config = args.target

    if os.getenv("TOOLING_DEBUG", False):
        print("DEBUG:")
        print(f"\t{connect_url}")
        print(f"\t{target_database_config}")

    database_setup(target_database_config, connect_url)
    print("done")


if __name__ == "__main__":
    main()
