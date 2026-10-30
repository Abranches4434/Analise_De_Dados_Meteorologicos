import os
from urllib.parse import quote_plus

from flask import Flask

from Entity import db
from Routes.EndPoints import registros_bp, thresholds_bp, localidades_bp

app = Flask(__name__)


#======== Configurando conexão com Banco ========

def _normalizarUrlBanco(url: str) -> str:
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]

    return url


def _obterUrlBanco() -> str:
    databaseUrl = os.getenv("DATABASE_URL")

    if databaseUrl:
        return _normalizarUrlBanco(databaseUrl)

    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")

    if not usuario or not senha:
        raise RuntimeError(
            "Configuração do banco ausente. Defina DATABASE_URL ou DB_USER e DB_PASSWORD."
        )

    host = os.getenv("DB_HOST", "localhost")
    porta = os.getenv("DB_PORT", "5432")
    nome = os.getenv("DB_NAME", "analiseMeteorologica")

    return (
        f"postgresql+psycopg://{quote_plus(usuario)}:{quote_plus(senha)}@"
        f"{host}:{porta}/{nome}"
    )


app.config["SQLALCHEMY_DATABASE_URI"] = _obterUrlBanco()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#======== Adicionando Blueprints à API ========

app.register_blueprint(registros_bp)
app.register_blueprint(thresholds_bp)
app.register_blueprint(localidades_bp)


#======== Comandos de banco ========

@app.cli.command("init-db")
def init_db():
    """Cria/verifica as tabelas no banco configurado."""
    with app.app_context():
        db.create_all()

    print("Tabelas criadas/verificadas com sucesso.")


#======== Inicializando API ========

if __name__ == "__main__":
    app.run(debug=True)
