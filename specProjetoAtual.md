# SpecProjetoAtual — Back-end

> Documento de estado atual do projeto. Deve ser atualizado após cada commit de implementação.
> Este arquivo descreve o que existe no código e no banco, não o que está planejado.

## 1. Identificação

| Item | Valor |
|---|---|
| Projeto | AnaliseDeDadosMeteorologicos |
| Diretório | `/home/kaique/Área de trabalho/AnaliseDeDadosMeteorologicos` |
| Branch | `main` |
| Último commit estável | `72b6d36` — Consolida configuração atual da API |
| Data desta atualização | 2026-10-30 |
| Estado da árvore Git | Limpa após o commit `72b6d36` |

## 2. Stack e versões

| Tecnologia | Versão |
|---|---|
| Python | 3.12 |
| Flask | 3.1.3 |
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
├── Controller/
├── DTOs/
├── Entity/
├── Enum/
├── Exception/
├── Repository/
├── Routes/
├── Service/
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
| UmidadeRelativa | numérico, 0 a 100 |
| Precipitacao | numérico, maior ou igual a 0 |
| VelocidadeVento | numérico, maior ou igual a 0 |
| PressaoAtmosferica | numérico, maior ou igual a 0 |
| Data | data |
| Hora | hora |
| Ativo | booleano, padrão verdadeiro |
| FKLocalidade | FK para Localidades |

Restrições: `TempMin <= TempMax` e unicidade de data, hora e localidade.

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
| GET | `/localidades` | Lista localidades |
| POST | `/localidades` | Cadastra localidade |
| GET | `/localidades/<id>` | Busca localidade |
| PUT | `/localidades/<id>` | Altera localidade |
| DELETE | `/localidades/<id>` | Remove localidade |
| GET | `/registros` | Lista registros |
| POST | `/registros` | Cadastra registro |
| GET | `/registros/<id>` | Busca registro |
| PUT | `/registros/<id>` | Altera registro |
| DELETE | `/registros/<id>` | Remove registro |
| GET | `/thresholds` | Lista thresholds |
| POST | `/thresholds` | Cadastra threshold |
| GET | `/thresholds/<id>` | Busca threshold |
| PUT | `/thresholds/<id>` | Altera threshold |
| DELETE | `/thresholds/<id>` | Remove threshold |

Formato de erro: `{"erro": "mensagem"}` com status 400, 404, 409 ou 500.

## 6. Regras de negócio implementadas

- Cadastro de localidades com nome, cidade, estado, latitude e longitude.
- Registro climático vinculado a uma localidade e a data/hora.
- Validação de faixas de temperatura (-20 a 50), umidade (0 a 100), precipitação, vento e pressão não negativos.
- Temperatura mínima não pode ser maior que a máxima.
- Data do registro não pode ser futura.
- Bloqueio de localidade duplicada por latitude e longitude.
- Bloqueio de registro duplicado por data, hora e localidade.
- Bloqueio de threshold duplicado por localidade, variável, tipo e estação.
- Validações específicas de thresholds por variável.
- Localidade com registros ou thresholds não pode ser excluída.
- Tratamento de erros de validação, não encontrado, conflito e erro interno.

## 7. Lacunas em relação ao escopo

- Não armazena temperatura média.
- Não possui consulta por período e localidade.
- Não gera estatísticas descritivas.
- Não compara localidades.
- Não identifica eventos extremos.
- Não analisa sazonalidade.
- Não exporta resultados.
- `DELETE` exclui fisicamente; não preserva histórico.
- Não possui interface gráfica.
- Não possui Dockerfile, docker-compose ou script SQL de inicialização.
- Não usa classes com herança, polimorfismo, construtor e encapsulamento de forma efetiva.
- A API usa Flask puro, não Flask-RESTful.
- Testes cobrem apenas a inicialização da aplicação.

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

- O schema do banco local está diferente do schema definido nos modelos atuais (tipos e nulabilidade), provavelmente por criação anterior com versões antigas dos modelos.
- O diretório `.venv` está versionado no Git, apesar de o `.gitignore` prever ambientes virtuais.
- A configuração de testes usa SQLite, que não é um SGBD permitido pelo trabalho.
- O README ainda não documenta as análises, a interface, o Docker nem o fluxo final.

## 11. Histórico de atualizações

| Data | Commit | Alteração documentada |
|---|---|---|
| 2026-10-30 | `72b6d36` | Estado inicial documentado antes da finalização; consolidada a configuração local com `python-dotenv` |
