from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from Entity.Localidades import Localidades
from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity.Thresholds import Thresholds