set dotenv-load

alembic_config := "app/database/migrations/alembic.ini"

# example: just server --port 8000 --host 0.0.0.0 
server *ARGS:
  DB_DEV=True \
  uv run fastapi dev --reload {{ ARGS }}

# example: just setup_db
setup_db:
  uv run tooling/setup_db.py -q --target fastapimessenger:fastapimessenger:fastapimessenger


# example: just alembic revision --autogenerate
alembic *ARGS:
  DB_DEV=True \
  uv run -m alembic -c {{ alembic_config }} {{ ARGS }}

# example: just test tests -v -s --log-cli-level=INFO
test target="tests" *ARGS:
  export SERVER_TESTING=true 
  export DB_URL="sqlite+aiosqlite:///:memory:"
  uv run pytest {{ target }} {{ ARGS }}

