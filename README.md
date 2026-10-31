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

A conexão com o banco é lida do arquivo `.env` na raiz do projeto, carregado automaticamente pelo `app.py`. A API falha na inicialização caso nenhuma configuração seja informada.

Edite o `.env` e preencha os parâmetros de conexão:

```bash
DATABASE_URL=postgresql://SEU_USUARIO:SUA_SENHA@localhost:5432/analiseMeteorologica
```

Também é possível usar os campos separados:

```bash
DB_USER=SEU_USUARIO
DB_PASSWORD=SUA_SENHA
DB_HOST=localhost
DB_PORT=5432
DB_NAME=analiseMeteorologica
```

O `.env.example` serve como modelo. Variáveis exportadas no shell também são aceitas e têm prioridade sobre o `.env`.

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
