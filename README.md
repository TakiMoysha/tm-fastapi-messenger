**Goal**: мессенджер с возможностью обмена сообщениями и создания групповых чатов, аналогичный Telegram.

**Gimmics**:

- WAL (PostgreSQL) for messages;
- keycloak for authentication & authorization;
- RS256 (asymmetric) for encrypting messages;

**Stack**:

- Python (FastAPI, asyncio);
- SQLAlchemy (ORM, асинхронные операции);
- Веб-сокетах (реализация real-time взаимодействия);
- Docker и Docker Compose (развертывание сервиса в контейнерах);
- Предотвращении дублирования сообщений при параллельной отправке.

**Tasks**:

1. Chat (WebSocket)

- models:

  - user (id, name, email, password)
  - chat (id, title, type: private/group)
  - group (id, title, creator_id, participants)
  - message (id, chat_id, sender_id, text, timestamp, is_read)

- Реализовать подключение пользователей через WebSocket.
- Обмен текстовыми сообщениями между пользователями в реально времени.
- Возможность создания групповых чатов.
- Сообщения должны сохраняться в PostgreSQL.
- Формат сообщений: `{ "id": int, "chat_id": int, "sender_id": int, "text": str, "timestamp": datetime, "is_read": bool }`

2. is_read flag set when message was read by all participants (group) or by one (private):

- Предотвращение дублирования сообщений при параллельной отправке (?).
- rest для всех истории (`/api/history/{chat_id}?limit=10&offset=0`)
- message order by timestamp

**Assessment**:

1. Architecture:

- controllers, services, repositories
- Dependency Injection

2. Code Quality:

- Clean, readable code
- No anti-patterns (? - which patterns)

3. Performance:

- Efficient SQL queries
- WebSocket optimization

4. Testing:

- chats working;
- exceptions handled;
- prevent message duplication; (? - idempotency)
- multiconnection (? - multiaccounts)
- jwt - oauth 2 / fastapi security
- unittests

[[./docs/database_schema.png]]

## References

()[https://github.com/amirhosss/FastAPI-RS256-MongoDB-Redis]
()[https://github.com/nsidnev/fastapi-realworld-example-app]
