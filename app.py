from flask import Flask
from Entity import db

app = Flask(__name__)

username = "Usuário respectivo"
password = "Senha respectiva"

app.config["SQLALCHEMY_DATABASE_URI"] = (f"postgresql://{username}:{password}@localhost:5432/analiseMeteorologica")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)