from flask import Flask
from Entity import db
from Routes.EndPoints import registros_bp,thresholds_bp,localidades_bp

app = Flask(__name__)


#======== Configurando conexão com Banco ========

username = "Usuário respectivo"
password = "Senha respectiva"

app.config["SQLALCHEMY_DATABASE_URI"] = (f"postgresql://{username}:{password}@localhost:5432/analiseMeteorologica")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#======== Adicionando Blueprints à API ========

app.register_blueprint(registros_bp)
app.register_blueprint(thresholds_bp)
app.register_blueprint(localidades_bp)


#======== Inicializando API ========

if __name__ == "__main__":
    app.run(debug=True)