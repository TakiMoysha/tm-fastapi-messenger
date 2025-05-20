set dotenv-load

alembic_config := "app/database/migrations/alembic.ini"

# ex: just server --port 8000 --host 0.0.0.0 
server *ARGS:
  DB_DEV=True \
  uv run fastapi dev --reload {{ ARGS }}

# ex: just fastapi prepare_db
fastapi *ARGS:
  uv run fastapi {{ ARGS }}

# ex: just setup_db
setup_db bootstrap_db="fastapimessenger:fastapimessenger:fastapimessenger":
  uv run tooling/setup_db.py -q --target {{ bootstrap_db }}


# ex: just alembic revision --autogenerate
alembic *ARGS:
  DB_DEV=True \
  uv run -m alembic -c {{ alembic_config }} {{ ARGS }}

# ex: just test tests -v -s --show-capture=all --log-cli-level=INFO
test target="tests" *ARGS:
  SERVER_TESTING=true  \
  DB_URL="sqlite+aiosqlite:///tmp/test.sqlite3" \
  uv run pytest {{ target }} {{ ARGS }}

