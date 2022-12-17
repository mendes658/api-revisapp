# REVISAPP API

### A API foi feita em Python usando FastAPI, ela se comunica com um banco PostgreSQL. No momento ela está hospedada em um servidor AWS EC2
### Como ela se comunica com um banco Postgre, é necessário criar uma database Postgre na sua máquina seguindo o schema na pasta 'database_creation_sql'

## Instala as dependências necessárias (é recomendado iniciar um virtual enviroment antes)
```
pip install -r requirements.txt
```

## Crie um arquivo chamado .env na pasta principal do projeto contento as seguintes informações:
```
DATABASE_HOSTNAME=localhost
DATABASE_PASSWORD=senha
DATABASE_USERNAME=username (geralmente é postgres)
DATABASE_NAME=nome da sua database
SECRET_KEY=uma sequência de caracteres aleatórios para a secret key do token jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
```

## Para subir num servidor de desenvolvimento
```
uvicorn app.main:app --reload --host 0.0.0.0
```