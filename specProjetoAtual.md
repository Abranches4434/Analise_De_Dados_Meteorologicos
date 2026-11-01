# SpecProjetoAtual — Back-end

> Documento de estado atual do projeto. Deve ser atualizado após cada commit de implementação.
> Este arquivo descreve o que existe no código e no banco, não o que está planejado.

## 1. Identificação

| Item | Valor |
|---|---|
| Projeto | AnaliseDeDadosMeteorologicos |
| Diretório | `/home/kaique/Área de trabalho/AnaliseDeDadosMeteorologicos` |
| Branch | `main` |
| Último commit estável | `5df74f2` — Documenta testes PostgreSQL e CI |
| Data desta atualização | 2026-10-31 |
| Estado da árvore Git | Limpa após o commit desta atualização |

## 2. Stack e versões

| Tecnologia | Versão |
|---|---|
| Python | 3.12 |
| Flask | 3.1.3 |
| Flask-RESTful | 0.3.10 |
| Flask-SQLAlchemy | 3.1.1 |
| SQLAlchemy | 2.1.6 |
| Pydantic | 2.14.1 |
| psycopg | 3.3.6 |
| python-dotenv | 1.2.4 |
| Banco | PostgreSQL |
| Testes | unittest com PostgreSQL 16 |

## 3. Estrutura atual

```text
AnaliseDeDadosMeteorologicos/
├── app.py
├── Config/
├── Controller/       # Controladores e BaseController
├── DTOs/             # Validação e serialização Pydantic
├── Entity/           # Modelos SQLAlchemy
├── Enum/             # Enums de domínio
├── Exception/        # Exceções de negócio
├── Repository/       # Repositórios e BaseRepository
├── Routes/           # Resources REST e BaseResource
├── Service/          # Serviços, BaseService e AnaliseService
├── seed.py           # Dados de demonstração
├── init.sql          # Script SQL de inicialização do PostgreSQL
├── Dockerfile
├── docker-compose.yml
├── tests/
└── requirements.txt
```

## 4. Modelo de dados atual

### Localidades

| Coluna | Tipo/modelo |
|---|---|
| IDLocalidade | inteiro, PK |
| Nome | texto, obrigatório |
| Cidade | texto, obrigatório |
| Estado | enum de UF |
| Latitude | numérico, entre -90 e 90 |
| Longitude | numérico, entre -180 e 180 |
| Ativo | booleano, padrão verdadeiro |

Restrição: latitude e longitude únicas.

Relacionamentos ORM: `registros` e `thresholds` (1:N), com `back_populates`
para `RegistrosClimaticos.localidade` e `Thresholds.localidade`.

### RegistrosClimaticos

| Coluna | Tipo/modelo |
|---|---|
| IDRegistrosClimaticos | inteiro, PK |
| TempMax | numérico, -20 a 50 |
| TempMin | numérico, -20 a 50 |
| TempMedia | numérico, -20 a 50 |
| UmidadeRelativa | numérico, 0 a 100 |
| Precipitacao | numérico, maior ou igual a 0 |
| VelocidadeVento | numérico, 0 a 150 |
| PressaoAtmosferica | numérico, 800 a 1100 |
| Data | data |
| Hora | hora |
| Ativo | booleano, padrão verdadeiro |
| FKLocalidade | FK para Localidades |

Restrições: `TempMin <= TempMax`, `TempMin <= TempMedia <= TempMax` e unicidade de data, hora e localidade.

Relacionamento ORM: `localidade` (N:1) com `Localidades.registros`.

### Thresholds

| Coluna | Tipo/modelo |
|---|---|
| IDThreshold | inteiro, PK |
| FKLocalidade | FK para Localidades |
| Variavel | enum de variável climática |
| TipoLimiar | MAXIMO, MINIMO ou DIASSEMCHUVA |
| EstacaoDoAno | PRIMAVERA, VERAO, OUTONO, INVERNO ou ANUAL |
| Valor | numérico |
| Ativo | booleano, padrão verdadeiro |

Restrição: unicidade de localidade, variável, tipo de limiar e estação do ano.

Relacionamento ORM: `localidade` (N:1) com `Localidades.thresholds`.

## 5. API atual

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está no ar |
| GET | `/localidades` | Lista localidades (aceita `incluir_inativos=true`) |
| POST | `/localidades` | Cadastra localidade |
| GET | `/localidades/<id>` | Busca localidade |
| PUT | `/localidades/<id>` | Altera localidade |
| DELETE | `/localidades/<id>` | Inativa localidade |
| GET | `/registros` | Lista registros; aceita `incluir_inativos`, `data_inicio`, `data_fim` e `localidade_id` |
| POST | `/registros` | Cadastra registro |
| GET | `/registros/<id>` | Busca registro |
| PUT | `/registros/<id>` | Altera registro |
| DELETE | `/registros/<id>` | Inativa registro |
| GET | `/thresholds` | Lista thresholds (aceita `incluir_inativos=true`) |
| POST | `/thresholds` | Cadastra threshold |
| GET | `/thresholds/<id>` | Busca threshold |
| PUT | `/thresholds/<id>` | Altera threshold |
| DELETE | `/thresholds/<id>` | Inativa threshold |
| GET | `/analises/estatisticas` | Média, mediana, máximo, mínimo e quantidade por variável |
| GET | `/analises/comparacao` | Compara duas ou mais localidades no mesmo período |
| GET | `/analises/eventos-extremos` | Lista eventos que atingiram thresholds ativos |
| GET | `/analises/sazonalidade` | Médias por mês (`agrupamento=mes`) ou estação (`agrupamento=estacao`) |
| GET | `/exportacoes/<tipo>` | Exporta CSV de registros, estatísticas, comparação, eventos ou sazonalidade |

As análises aceitam `data_inicio`, `data_fim` e `localidade_id`; a comparação usa `localidade_ids=1,2`; a exportação usa os mesmos filtros e aceita `agrupamento`. Datas no formato `AAAA-MM-DD`.

Formato de erro: `{"erro": "mensagem"}` com status 400, 404, 409 ou 500. As rotas são implementadas com `flask_restful.Resource`; os controladores não dependem de HTTP e os services concentram as regras de negócio.

## 6. Regras de negócio implementadas

- Cadastro de localidades com nome, cidade, estado, latitude e longitude.
- Registro climático vinculado a uma localidade e a data/hora.
- Validação de faixas de temperatura (-20 a 50), umidade (0 a 100), precipitação não negativa, vento (0 a 150) e pressão (800 a 1100).
- Temperatura mínima não pode ser maior que a máxima e a média deve ficar entre as duas.
- Data do registro não pode ser futura.
- Bloqueio de localidade duplicada por latitude e longitude.
- Bloqueio de registro duplicado por data, hora e localidade.
- Bloqueio de threshold duplicado por localidade, variável, tipo e estação.
- Validações específicas de thresholds por variável.
- Registros, localidades e thresholds são inativados, não excluídos fisicamente.
- Registros só podem ser vinculados a localidades ativas.
- Tratamento de erros de validação, não encontrado, conflito e erro interno.
- Consulta de registros por período e localidade.
- Estatísticas descritivas: média, mediana, máximo, mínimo e quantidade.
- Comparação de duas ou mais localidades no mesmo intervalo.
- Eventos extremos por `MAXIMO`, `MINIMO` e `DIASSEMCHUVA`, respeitando a estação do threshold.
- Sazonalidade por mês ou estação do hemisfério sul.
- Exportação CSV com separador `;`, BOM UTF-8 e cabeçalhos em português.
- Seed de demonstração com 3 localidades, 1.095 registros e 18 thresholds.

## 7. Lacunas em relação ao escopo

- Nenhuma lacuna de back-end identificada. A interface Tkinter permanece em projeto separado e não é containerizada.

## 8. Configuração e execução

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configurar `.env` com `DATABASE_URL` ou com `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` e `DB_NAME`.

```bash
flask --app app init-db
flask --app app seed-demo
python app.py
```

O comando `seed-demo` só cria dados se ainda não existirem localidades. Os dados de demonstração usam o ano de 2025, três cidades paulistas e thresholds anuais/verão/inverno.

### Docker

O `Dockerfile` usa `python:3.12-slim`, instala `requirements.txt` e executa `python app.py`. O `docker-compose.yml` define PostgreSQL 16, volume persistente, healthchecks e a API com `DATABASE_URL` apontando para o serviço `db`. O `init.sql` cria os enums e as tabelas com as mesmas constraints do modelo SQLAlchemy e é executado pelo entrypoint do PostgreSQL na primeira criação do volume.

A API é iniciada após o banco ficar saudável, executa `flask --app app init-db`, `flask --app app seed-demo` e sobe em `0.0.0.0:5000`. Portas, banco e credenciais podem ser alterados pelas variáveis `API_PORT`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD`.

## 9. Testes

```bash
python -m unittest discover -s tests -v
```

Estado atual: 16 testes, divididos em inicialização e integração, executados com PostgreSQL. A suíte usa o schema isolado `analise_meteorologica_test`, criado e recriado automaticamente, e obtém a conexão de `TEST_DATABASE_URL` ou `DATABASE_URL`; não utiliza SQLite.

Os testes de integração cobrem seed, estatísticas, comparação, eventos extremos, sazonalidade por mês e estação, exportação dos cinco tipos de CSV, CRUD, inativação, exclusão de registros inativos das análises, semântica `MAXIMO >= limiar`, `MINIMO <= limiar`, `DIASSEMCHUVA`, relacionamentos ORM e erros de validação.

O Docker Compose foi validado com `docker compose config`, build da imagem, subida de PostgreSQL e API, healthcheck, seed automático, CRUD, as quatro análises, exportação CSV e chamadas pelo cliente da interface. Os containers e o volume de teste foram removidos ao final. A suíte também foi executada contra um PostgreSQL 16 isolado via Docker, reproduzindo o ambiente do CI.

O workflow `.github/workflows/ci.yml` configura PostgreSQL 16, valida a sintaxe, valida o Docker Compose e executa os testes.

## 10. Problemas conhecidos

- O schema local foi recriado com `DROP SCHEMA public CASCADE`; os dados anteriores foram descartados conforme decisão do grupo.
- As constraints de `CHECK` das entidades precisaram de identificadores entre aspas para funcionar no PostgreSQL.
- O diretório `.venv` foi removido do índice do Git e permanece apenas localmente.
- A API foi validada com `flask run` e com Docker Compose, incluindo `/health`, CRUD, análises e exportação CSV em PostgreSQL.
- O CI está configurado para PostgreSQL 16; a execução local equivalente passou com 16 testes.
- O banco local contém os dados de demonstração do comando `seed-demo`.

## 11. Histórico de atualizações

| Data | Commit | Alteração documentada |
|---|---|---|
| 2026-10-30 | `72b6d36` | Estado inicial documentado antes da finalização; consolidada a configuração local com `python-dotenv` |
| 2026-10-30 | `69ca9e6` | Adicionados `TempMedia`, faixas de vento e pressão, inativação de registros e recriação do schema PostgreSQL |
| 2026-10-30 | `522441c` | API migrada para Flask-RESTful com `BaseRepository`, `BaseService`, `BaseController` e `BaseResource`; adicionado `/health` |
| 2026-10-30 | `5d729d0` | Adicionadas consultas filtradas, estatísticas, comparação, eventos extremos, sazonalidade, exportação CSV e seed de demonstração |
| 2026-10-30 | `186876c` | Adicionados Dockerfile, docker-compose, `init.sql` e configuração de host/porta/debug por variáveis de ambiente; README atualizado |
| 2026-10-30 | `8b9650b` | Testes migrados para PostgreSQL com schema isolado; adicionados testes de integração e CI com PostgreSQL 16 |
| 2026-10-30 | `5df74f2` | Documentação dos testes PostgreSQL e do workflow de CI atualizada |
| 2026-10-31 | — | Adicionados relacionamentos `relationship()` nas entidades, teste de relacionamentos ORM e remoção do `.venv` do índice do Git |
