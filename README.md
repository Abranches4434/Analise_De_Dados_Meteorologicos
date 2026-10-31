# Analise_De_Dados_Meteorologicos

Sistema para armazenamento de dados climáticos históricos, consulta por período e
localidade, análises estatísticas e exportação CSV. O projeto possui uma API REST em
Flask e uma interface desktop Tkinter em projeto separado.

## Funcionalidades

- Cadastro, consulta, alteração e inativação de localidades, registros e thresholds.
- Filtros de registros por data inicial, data final e localidade.
- Estatísticas descritivas: média, mediana, máximo, mínimo e quantidade.
- Comparação de duas ou mais localidades no mesmo período.
- Detecção de eventos extremos com thresholds anuais ou sazonais.
- Sazonalidade por mês ou por estação do ano.
- Exportação CSV de registros, estatísticas, comparação, eventos e sazonalidade.
- Seed com 3 localidades, 1.095 registros e 18 thresholds de demonstração.
- Interface Tkinter com abas de localidades, registros, thresholds e análises.

## Stack

| Tecnologia | Versão/uso |
|---|---|
| Python | 3.12 |
| Flask | 3.1.3 |
| Flask-RESTful | 0.3.10 |
| Flask-SQLAlchemy | 3.1.1 |
| SQLAlchemy | 2.1.6 |
| Pydantic | 2.14.1 |
| psycopg | 3.3.6 |
| PostgreSQL | 16 no Docker Compose |
| Tkinter | Interface desktop, sem dependências externas |
| Docker Compose | API + banco de dados |

## Estrutura

```text
AnaliseDeDadosMeteorologicos/
├── app.py                  # Aplicação Flask, configuração e comandos CLI
├── seed.py                 # Dados de demonstração
├── init.sql                # Script SQL de inicialização do PostgreSQL
├── Dockerfile
├── docker-compose.yml
├── Config/
├── Controller/
├── DTOs/
├── Entity/
├── Enum/
├── Exception/
├── Repository/
├── Routes/
├── Service/
└── tests/
```

A interface está em `../InterfaceAnaliseMeteorologica`.

## Execução com Docker

O Docker Compose cria o PostgreSQL, aplica `init.sql`, inicia a API, verifica as tabelas
e popula os dados de demonstração caso o banco esteja vazio.

```bash
docker compose up --build -d
```

A API fica disponível em `http://127.0.0.1:5000` e o PostgreSQL em
`localhost:5432`. Os valores padrão podem ser alterados por variáveis de ambiente.

| Variável | Padrão |
|---|---|
| `POSTGRES_DB` | `analiseMeteorologica` |
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_PASSWORD` | `postgres` |
| `POSTGRES_PORT` | `5432` |
| `API_PORT` | `5000` |

Exemplo com portas alternativas, útil quando já existe um PostgreSQL local:

```bash
POSTGRES_PORT=5433 API_PORT=5001 docker compose up --build -d
```

Comandos úteis:

```bash
docker compose ps
docker compose logs -f api
curl http://127.0.0.1:5000/health
docker compose down
```

O `init.sql` é executado apenas na primeira criação do volume. Para recriar o banco e
reaplicar o script, remova o volume com `docker compose down -v`.

## Execução local

Requisitos: Python 3.12 e PostgreSQL.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie o banco `analiseMeteorologica` e configure o `.env` a partir de `.env.example`:

```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/analiseMeteorologica
```

Também são aceitos `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` e `DB_NAME`.
Variáveis exportadas no shell têm prioridade sobre o `.env`.

Crie as tabelas e os dados de demonstração:

```bash
flask --app app init-db
flask --app app seed-demo
```

Inicie a API:

```bash
python app.py
# ou
flask --app app run
```

O host, a porta e o modo debug podem ser configurados por `FLASK_HOST`, `FLASK_PORT` e
`FLASK_DEBUG`. Os padrões são `0.0.0.0`, `5000` e desativado.

O servidor embutido do Flask é adequado para desenvolvimento e demonstração local. Para
produção seria necessário um servidor WSGI dedicado, fora do escopo deste trabalho.

## Interface Tkinter

Em outro terminal, a partir de `../InterfaceAnaliseMeteorologica`:

```bash
python3 main.py
```

A interface usa `API_URL` (padrão `http://127.0.0.1:5000`) e `API_TIMEOUT` (padrão 15
segundos). Para apontar para uma API em outra porta:

```bash
API_URL=http://127.0.0.1:5001 python3 main.py
```

A API deve estar em execução antes de abrir a interface.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está no ar |
| GET | `/localidades` | Lista localidades; aceita `incluir_inativos=true` |
| POST | `/localidades` | Cadastra localidade |
| GET | `/localidades/<id>` | Busca localidade |
| PUT | `/localidades/<id>` | Altera localidade |
| DELETE | `/localidades/<id>` | Inativa localidade |
| GET | `/registros` | Lista registros; aceita `incluir_inativos`, `data_inicio`, `data_fim` e `localidade_id` |
| POST | `/registros` | Cadastra registro |
| GET | `/registros/<id>` | Busca registro |
| PUT | `/registros/<id>` | Altera registro |
| DELETE | `/registros/<id>` | Inativa registro |
| GET | `/thresholds` | Lista thresholds; aceita `incluir_inativos=true` |
| POST | `/thresholds` | Cadastra threshold |
| GET | `/thresholds/<id>` | Busca threshold |
| PUT | `/thresholds/<id>` | Altera threshold |
| DELETE | `/thresholds/<id>` | Inativa threshold |
| GET | `/analises/estatisticas` | Estatísticas por variável |
| GET | `/analises/comparacao` | Compara localidades (`localidade_ids=1,2`) |
| GET | `/analises/eventos-extremos` | Eventos que atingiram thresholds ativos |
| GET | `/analises/sazonalidade` | Médias por mês ou estação (`agrupamento=mes\|estacao`) |
| GET | `/exportacoes/<tipo>` | CSV de registros, estatísticas, comparação, eventos ou sazonalidade |

As análises e exportações aceitam `data_inicio`, `data_fim` e `localidade_id`, com datas
no formato `AAAA-MM-DD`. A exportação de comparação também aceita `localidade_ids` e
`agrupamento`.

Erros são retornados como `{"erro": "mensagem"}` com status 400, 404, 409 ou 500.

## Regras principais

- Registros, localidades e thresholds são inativados, não excluídos fisicamente.
- Análises consideram apenas registros ativos por padrão.
- `MAXIMO` é atingido quando o valor é maior ou igual ao limiar; `MINIMO`, quando é menor
  ou igual.
- `DIASSEMCHUVA` conta dias secos consecutivos conforme o limiar e a estação.
- A sazonalidade segue as estações do hemisfério sul.
- O CSV usa separador `;`, BOM UTF-8 e cabeçalhos em português.

## Testes

```bash
python -m unittest discover -s tests -v
```

A validação da API também pode ser feita com `curl` ou pela interface. O Docker Compose
inclui healthcheck para o banco e para a API.
