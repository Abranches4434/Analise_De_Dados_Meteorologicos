import os
from pathlib import Path
from urllib.parse import quote_plus

import psycopg
from dotenv import dotenv_values
from psycopg import sql
from sqlalchemy import text
from sqlalchemy.engine import make_url


BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_TESTE = "analise_meteorologica_test"


def _url_configurada() -> str:
    url = os.getenv("DATABASE_URL")

    if url:
        return url

    valores = dotenv_values(BASE_DIR / ".env")
    url = valores.get("DATABASE_URL")

    if url:
        return url

    usuario = os.getenv("DB_USER") or valores.get("DB_USER")
    senha = os.getenv("DB_PASSWORD") or valores.get("DB_PASSWORD")

    if not usuario or senha is None:
        raise RuntimeError(
            "Configure DATABASE_URL ou TEST_DATABASE_URL para os testes."
        )

    host = os.getenv("DB_HOST") or valores.get("DB_HOST") or "localhost"
    porta = os.getenv("DB_PORT") or valores.get("DB_PORT") or "5432"
    nome = (
        os.getenv("DB_NAME")
        or valores.get("DB_NAME")
        or "analiseMeteorologica"
    )

    return (
        f"postgresql://{quote_plus(usuario)}:{quote_plus(senha)}@"
        f"{host}:{porta}/{nome}"
    )


def _url_teste():
    url = make_url(
        os.getenv("TEST_DATABASE_URL") or _url_configurada()
    )

    if not url.drivername.startswith("postgresql"):
        raise RuntimeError("Os testes de integração exigem PostgreSQL.")

    return url


def _criar_schema(url):
    with psycopg.connect(
        host=url.host or "localhost",
        port=url.port or 5432,
        user=url.username,
        password=url.password,
        dbname=url.database,
        autocommit=True,
    ) as conexao:
        conexao.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(SCHEMA_TESTE)
            )
        )


def preparar_ambiente():
    url = _url_teste()
    _criar_schema(url)
    url = url.update_query_dict(
        {"options": f"-csearch_path={SCHEMA_TESTE}"}
    )
    os.environ["DATABASE_URL"] = url.render_as_string(
        hide_password=False
    )
    os.environ.setdefault("FLASK_DEBUG", "false")
    return url


def resetar_banco(app, db):
    with app.app_context():
        db.session.remove()
        db.session.execute(
            text(f'DROP SCHEMA IF EXISTS "{SCHEMA_TESTE}" CASCADE')
        )
        db.session.execute(
            text(f'CREATE SCHEMA "{SCHEMA_TESTE}"')
        )
        db.session.commit()
        db.create_all()
