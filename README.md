# Aplicação Flask com Arquitetura Hexagonal

Aplicação para cadastrar e consultar endereços por CEP. O núcleo depende de ports abstratos (`ABC`), e os adapters concretos são injetados na criação do Flask. A escolha de persistência e a origem das consultas por CEP são independentes.

## Executar no Windows

Na raiz do projeto, pelo PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r app\requirements.txt
python -m app.app
```

Por padrão, a aplicação usa SQLite e consulta CEPs cadastrados localmente. Na primeira execução, são criados 50 endereços de demonstração em `app/enderecos.db`.

## Arquitetura

- `app/domain/ports`: contratos abstratos para persistência e consulta de CEP.
- `app/service`: regras de validação e casos de uso; depende somente dos ports.
- `app/adapters/persistence`: implementações SQLite e PostgreSQL do port de persistência.
- `app/adapters/cep_lookup`: consulta no repositório selecionado ou na API dos Correios.
- `app/presentation`: endpoints Flask, que encaminham solicitações ao serviço.
- `app/__init__.py`: composition root; cria e injeta os adapters configurados.

## Configuração

| Variável | Valores | Padrão / uso |
| --- | --- | --- |
| `DATABASE_ADAPTER` | `sqlite`, `postgres` | `sqlite` seleciona a persistência. |
| `SQLITE_DATABASE_PATH` | caminho de arquivo | `app/enderecos.db`. |
| `DATABASE_URL` | URL PostgreSQL | Obrigatória para `DATABASE_ADAPTER=postgres`, por exemplo `postgresql://app_user:app_password@localhost:5432/app_db`. |
| `CEP_LOOKUP_ADAPTER` | `database`, `correios` | `database` consulta o banco selecionado. |
| `CORREIOS_API_URL` | URL base | Padrão `https://api.correios.com.br/cep/v1/enderecos`. |
| `CORREIOS_API_TOKEN` | token Bearer | Obrigatório para `CEP_LOOKUP_ADAPTER=correios`; informe um token válido obtido junto aos Correios. |

No VS Code, selecione uma das quatro configurações em `.vscode/launch.json`. Para os perfis PostgreSQL, defina `DATABASE_URL` no ambiente do VS Code. Para os perfis Correios, defina `CORREIOS_API_TOKEN` no ambiente do VS Code. Não salve credenciais no arquivo de configuração.

O adapter Correios usa a API oficial autenticada; o acesso depende de credenciais e disponibilidade do serviço contratado. A instalação da dependência `psycopg` é necessária para selecionar PostgreSQL.

## API

- `GET /api/enderecos` lista os endereços persistidos.
- `GET /api/enderecos?cep=01001-000` pesquisa usando a origem definida em `CEP_LOOKUP_ADAPTER`.
- `GET /api/enderecos/cep/01001-000` consulta um CEP e retorna `404` quando não encontrado.
- `POST /api/enderecos` cadastra um endereço com JSON:

```json
{
  "cep": "12345-678",
  "logradouro": "Rua das Flores",
  "bairro": "Centro",
  "cidade": "Campinas",
  "uf": "SP"
}
```