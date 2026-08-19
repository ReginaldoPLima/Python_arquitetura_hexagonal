# Python Arquitetura Hexagonal

Aplicacao basica com Flask e banco de dados PostgreSQL executado via Docker.

## Pre-requisitos no Windows 11

Instale o [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/) e habilite o backend **WSL 2** durante a instalacao. Abra o Docker Desktop e aguarde o status `Engine running` antes de executar os comandos abaixo.

Confirme a instalacao em um novo PowerShell:

```powershell
docker --version
docker info
```

## Executar a aplicacao Flask

No PowerShell, a partir da raiz do projeto:

```powershell
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r app\requirements.txt
python app\app.py
```

A aplicacao ficara disponivel em http://localhost:5000.

## Criar e executar o PostgreSQL

Construa a imagem do banco:

```powershell
docker build -t arquitetura-postgres ./banco
```

Crie um volume nomeado e suba o container:

```powershell
docker volume create postgres_data
docker run --name arquitetura-postgres -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d arquitetura-postgres
```

O banco sera criado com os seguintes dados:

- Banco: `app_db`
- Usuario: `app_user`
- Senha: `app_password`
- Host: `localhost`
- Porta: `5432`

## Gerenciar o banco

Verifique o container:

```powershell
docker ps
docker logs arquitetura-postgres
```

Pare ou inicie o container:

```powershell
docker stop arquitetura-postgres
docker start arquitetura-postgres
```

Para remover apenas o container, mantendo os dados no volume:

```powershell
docker rm -f arquitetura-postgres
```

Depois, recrie o container usando o mesmo volume `postgres_data`.

Para remover permanentemente os dados do banco:

```powershell
docker volume rm postgres_data
```