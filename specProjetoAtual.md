# SpecProjetoAtual — Back-end

> Documento de estado atual do projeto. Deve ser atualizado após cada commit de implementação.
> Este arquivo descreve o que existe no código e no banco, não o que está planejado.

## 1. Identificação

| Item | Valor |
|---|---|
| Projeto | AnaliseDeDadosMeteorologicos |
| Diretório | `/home/kaique/Área de trabalho/AnaliseDeDadosMeteorologicos` |
| Branch | `main` |
| Último commit estável | `522441c` — Migra API para Flask-RESTful com camadas orientadas a objetos |
| Data desta atualização | 2026-10-30 |
| Estado da árvore Git | Limpa após o commit `522441c` (exceto caches do `.venv` versionado) |

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
| Testes | unittest |

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
├── Service/          # Serviços e BaseService
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

## 5. API atual

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está no ar |
| GET | `/localidades` | Lista localidades (aceita `incluir_inativos=true`) |
| POST | `/localidades` | Cadastra localidade |
| GET | `/localidades/<id>` | Busca localidade |
| PUT | `/localidades/<id>` | Altera localidade |
| DELETE | `/localidades/<id>` | Inativa localidade |
| GET | `/registros` | Lista registros (aceita `incluir_inativos=true`) |
| POST | `/registros` | Cadastra registro |
| GET | `/registros/<id>` | Busca registro |
| PUT | `/registros/<id>` | Altera registro |
| DELETE | `/registros/<id>` | Inativa registro |
| GET | `/thresholds` | Lista thresholds (aceita `incluir_inativos=true`) |
| POST | `/thresholds` | Cadastra threshold |
| GET | `/thresholds/<id>` | Busca threshold |
| PUT | `/thresholds/<id>` | Altera threshold |
| DELETE | `/thresholds/<id>` | Inativa threshold |

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

## 7. Lacunas em relação ao escopo

- Não possui consulta por período e localidade.
- Não gera estatísticas descritivas.
- Não compara localidades.
- Não identifica eventos extremos.
- Não analisa sazonalidade.
- Não exporta resultados.
- Não possui interface gráfica.
- Não possui Dockerfile, docker-compose ou script SQL de inicialização.
- Ainda não possui consultas, análises e exportação.
- Testes cobrem apenas inicialização, rotas e `/health`.

## 8. Configuração e execução

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configurar `.env` com `DATABASE_URL` ou com `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` e `DB_NAME`.

```bash
flask --app app init-db
python app.py
```

## 9. Testes

```bash
python -m unittest discover -s tests -v
```

Estado atual: 4 testes de inicialização, executados com SQLite em memória.

## 10. Problemas conhecidos

- O schema local foi recriado com `DROP SCHEMA public CASCADE`; os dados anteriores foram descartados conforme decisão do grupo.
- As constraints de `CHECK` das entidades precisaram de identificadores entre aspas para funcionar no PostgreSQL.
- O diretório `.venv` está versionado no Git, apesar de o `.gitignore` prever ambientes virtuais.
- A configuração de testes ainda usa SQLite, que não é um SGBD permitido pelo trabalho.
- O README ainda não documenta as análises, a interface, o Docker nem o fluxo final.
- A API foi validada com `flask run`, chamada real a `/health` e CRUD via test client em PostgreSQL.

## 11. Histórico de atualizações

| Data | Commit | Alteração documentada |
|---|---|---|
| 2026-10-30 | `72b6d36` | Estado inicial documentado antes da finalização; consolidada a configuração local com `python-dotenv` |
| 2026-10-30 | `69ca9e6` | Adicionados `TempMedia`, faixas de vento e pressão, inativação de registros e recriação do schema PostgreSQL |
| 2026-10-30 | `522441c` | API migrada para Flask-RESTful com `BaseRepository`, `BaseService`, `BaseController` e `BaseResource`; adicionado `/health` |
