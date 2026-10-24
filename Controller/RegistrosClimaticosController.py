from flask import jsonify
from DTOs.RegistrosClimaticosRequestDTO import RegistrosClimaticosRequestDTO
from DTOs.RegistrosClimaticosResponseDTO import RegistrosClimaticosReponseDTO

##COLOCAR OS REQUESTS AQUI

def inserirRegistro(Registro : RegistrosClimaticosRequestDTO) -> RegistrosClimaticosReponseDTO:
    return jsonify({
        "mensagem" : "Criando Registro"
    }), 201

def selecionarTodosRegistros() -> RegistrosClimaticosReponseDTO:
    return jsonify({
        "mensagem" : "Selecionando todos os Registros"
    }), 200

def selecionarRegistroPeloID(id : int) -> RegistrosClimaticosReponseDTO:
    return jsonify({
        "mensagem" : f"Selecionando Registro de Id: {id}"
    }), 200

def alterarRegistro(Registro : RegistrosClimaticosRequestDTO) -> RegistrosClimaticosReponseDTO:
    return jsonify({
        "mensagem" : "Alterando registro"
    }), 200

def deletarRegistroPeloId(id : int) -> RegistrosClimaticosReponseDTO:
    return jsonify({
        "mensagem" : f"Deletando Registro com Id: {id}"
    }), 204