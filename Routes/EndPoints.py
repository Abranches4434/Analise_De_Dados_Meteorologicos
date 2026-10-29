from flask import Blueprint, request
from Controller.LocalidadesController import *
from Controller.RegistrosClimaticosController import *
from Controller.ThresholdsController import *

#============ Definindo Blueprints de cada Controller ============

localidades_bp = Blueprint("localidades",__name__)
registros_bp = Blueprint("registros",__name__)
thresholds_bp = Blueprint("thresholds",__name__)

#============ Mapeamento de rotas das Localidades ============

@localidades_bp.route("/localidades", methods = ["GET"])
def RotaSelecionarTodasLocalidades():
        return selecionarTodasLocalidades()

@localidades_bp.route("/localidades/<int:id>", methods = ["GET"])
def RotaSelecionarLocalidadePeloID(id):
        return selecionarLocalidadePeloID(id)

@localidades_bp.route("/localidades", methods = ["POST"])
def RotaInserirLocalidade():
        objeto = request.get_json()
        return inserirLocalidade(objeto)

@localidades_bp.route("/localidades/<int:id>", methods = ["PUT"])
def RotaAlterarLocalidade(id):
        objeto = request.get_json()
        objeto["IDLocalidade"] = id
        return alterarLocalidade(objeto)

@localidades_bp.route("/localidades/<int:id>", methods = ["DELETE"])
def RotaDeletarLocalidadePeloId(id):
        return deletarLocalidadePeloId(id)

#============ Mapeamento de rotas dos Registros ============

@registros_bp.route("/registros", methods = ["GET"])
def RotaSelecionarTodosRegistros():
        return selecionarTodosRegistros()

@registros_bp.route("/registros/<int:id>", methods = ["GET"])
def RotaSelecionarRegistroPeloID(id):
        return selecionarRegistroPeloID(id)

@registros_bp.route("/registros", methods = ["POST"])
def RotaInserirRegistro():
        objeto = request.get_json()
        return inserirRegistro(objeto)

@registros_bp.route("/registros", methods = ["PUT"])
def RotaAlterarRegistro():
        objeto = request.get_json()
        return alterarRegistro(objeto)

@registros_bp.route("/registros/<int:id>", methods = ["DELETE"])
def RotaDeletarRegistroPeloId(id):
        return deletarRegistroPeloId(id)

#============ Mapeamento de rotas das Thresholds ============

@thresholds_bp.route("/thresholds", methods = ["GET"])
def RotaSelecionarTodasThresholds():
        return selecionarTodasThresholds()

@thresholds_bp.route("/thresholds/<int:id>", methods = ["GET"])
def RotaSelecionarThresholdPeloID(id):
        return selecionarThresholdPeloID(id)

@thresholds_bp.route("/thresholds", methods = ["POST"])
def RotaInserirThreshold():
        objeto = request.get_json()
        return inserirThreshold(objeto)

@thresholds_bp.route("/thresholds", methods = ["PUT"])
def RotaAlterarThreshold():
        objeto = request.get_json()
        return alterarThreshold(objeto)

@thresholds_bp.route("/thresholds/<int:id>", methods = ["DELETE"])
def RotaDeletarThresholdPeloId(id):
        return deletarThresholdPeloId(id)
