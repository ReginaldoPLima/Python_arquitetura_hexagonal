# Aplicação Flask em Camadas

Aplicação tradicional em camadas para cadastrar e buscar endereços pelo CEP. As rotas da camada de apresentação chamam a camada de serviço, que aplica validações e usa o repositório para acessar o SQLite. Na primeira execução, são criados 50 registros de demonstração em `app/enderecos.db`.

## Executar no Windows

Na raiz do projeto, pelo PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r app\requirements.txt
python -m app.app
```

Acesse http://localhost:5000. O SQLite faz parte da biblioteca padrão do Python, então não é necessário iniciar um servidor de banco ou Docker.

## Camadas

- `app/presentation`: rotas Flask e comunicação HTTP.
- `app/service`: validação e regras da aplicação.
- `app/repository`: persistência e consultas SQLite.
- `app/templates`: tela de busca e cadastro.

## API

- `GET /api/enderecos` lista os endereços.
- `GET /api/enderecos?cep=01001-000` busca pelo CEP.
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