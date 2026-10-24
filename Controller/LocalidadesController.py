from flask import jsonify
from DTOs.LocalidadesRequestDTO  import LocalidadesRequestDTO
from DTOs.LocalidadesResponseDTO import LocalidadesResponseDTO

##COLOCAR OS REQUESTS AQUI

def inserirLocalidade(Localidade : LocalidadesRequestDTO) -> LocalidadesResponseDTO:
    return jsonify({
        "mensagem" : "Criando Localidade"
    }), 201

def selecionarTodasLocalidades() -> LocalidadesResponseDTO:
    return jsonify({
        "mensagem" : "Selecionando todas as Localidades"
    }), 200

def selecionarLocalidadePeloID(id : int) -> LocalidadesResponseDTO:
    return jsonify({
        "mensagem" : f"Selecionando Localidade de Id: {id}"
    }), 200

def alterarLocalidade(Localidade : LocalidadesRequestDTO) -> LocalidadesResponseDTO:
    return jsonify({
        "mensagem" : "Alterando localidade"
    }), 200

def deletarLocalidadePeloId(id : int) -> LocalidadesResponseDTO:
    return jsonify({
        "mensagem" : f"Deletando Localidade com Id: {id}"
    }), 204