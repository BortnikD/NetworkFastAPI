# Example of a backend for a network 🌐
This project is an simple example of how you can organize a backend for your social network.  
Here I practice clean architecture principles to ensure the application is reliable, maintainable and scalable.

## Technologies ⚙️
- _FastAPI_
- _SQLAlchemy (postgres)_
- _alembic_


## Installation ⬇️
1. Clone the repository
```bash
git clone https://github.com/BortnikD/networkBackendFastApi.git
```

2. Set requirements
```bash
pip install -r requirements.txt
```

3. Set env variables
```bash
set AUTH_KEY "your_api_key_hex_32"
set DATABASE "your_database_name"
set POSTGRES_USER "your_username"
set POSTGRES_PORT "your_port"
set POSTGRES_PASSWORD "your_password"

```

4. Start the server 🚀
```bash
uvicorn app.main:app --reload
```