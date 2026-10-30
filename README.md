# Analise_De_Dados_Meteorologicos

Sistema voltado ao armazenamento de dados climáticos históricos e à geração de estatísticas, comparações e consultas por período e localidade.

## Requisitos

- Python >= 3.10 (versão recomendada e fixada: 3.12)
- PostgreSQL

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração

A conexão com o banco é lida de variáveis de ambiente. A API falha na inicialização caso nenhuma configuração seja informada.

Opção 1 — URL completa:

```bash
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/analiseMeteorologica"
```

Opção 2 — campos separados:

```bash
export DB_USER="usuario"
export DB_PASSWORD="senha"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="analiseMeteorologica"
```

Consulte `.env.example` para um modelo. O arquivo `.env` não é carregado automaticamente; exporte as variáveis no shell ou use sua ferramenta de preferência.

## Banco de dados

Crie/verifique as tabelas de forma controlada:

```bash
flask --app app init-db
```

## Execução

```bash
python app.py
# ou
flask --app app run
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Endpoints

- `GET|POST /localidades`
- `GET|PUT|DELETE /localidades/<id>`
- `GET|POST /registros`
- `GET|PUT|DELETE /registros/<id>`
- `GET|POST /thresholds`
- `GET|PUT|DELETE /thresholds/<id>`
