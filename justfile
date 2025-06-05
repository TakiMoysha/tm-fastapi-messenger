set dotenv-load

alembic_config := "app/database/migrations/alembic.ini"

# ex: just server --port 8000 --host 0.0.0.0 
server *ARGS: setup_db
  DB_DEV=true \
  SERVER_DEBUG=true \
  LOGGING_APP_LEVEL=DEBUG \
  uv run fastapi dev --reload {{ ARGS }}

# ex: just stage --workers 2
stage *ARGS:
  DB_DEV=True \
  uv run uvicorn app.main:application --host 0.0.0.0 --port 8000 {{ ARGS }}

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

# ex: just test tests/integration -v -s --show-capture=all --log-cli-level=INFO
test target="tests" *ARGS:
  SERVER_DEBUG=true \
  SERVER_TESTING=true  \
  LOGGING_APP_LEVEL=DEBUG \
  DB_URL="sqlite+aiosqlite:///tmp/test.sqlite3" \
  uv run pytest --disable-warnings {{ target }} {{ ARGS }}

