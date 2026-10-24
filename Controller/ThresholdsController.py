from flask import jsonify
from DTOs.ThresholdsRequestDTO import ThresholdsRequestDTO
from DTOs.ThresholdsResponseDTO import ThresholdsResponseDTO


##COLOCAR OS REQUESTS AQUI

def inserirThreshold(Threshold : ThresholdsRequestDTO) -> ThresholdsResponseDTO:
    return jsonify({
        "mensagem" : "Criando Threshold"
    }), 201

def selecionarTodasThresholds() -> ThresholdsResponseDTO:
    return jsonify({
        "mensagem" : "Selecionando todas as Thresholds"
    }), 200

def selecionarThresholdPeloID(id : int) -> ThresholdsResponseDTO:
    return jsonify({
        "mensagem" : f"Selecionando Threshold de Id: {id}"
    }), 200

def alterarThreshold(Threshold : ThresholdsRequestDTO) -> ThresholdsResponseDTO:
    return jsonify({
        "mensagem" : "Alterando Threshold"
    }), 200

def deletarThresholdPeloId(id : int) -> ThresholdsResponseDTO:
    return jsonify({
        "mensagem" : f"Deletando Threshold com Id: {id}"
    }), 204