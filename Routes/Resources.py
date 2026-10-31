from flask import request
from flask_restful import Resource

from Controller.LocalidadesController import LocalidadesController
from Controller.RegistrosClimaticosController import (
    RegistrosClimaticosController,
)
from Controller.ThresholdsController import ThresholdsController
from Routes.BaseResource import BaseResource


class LocalidadesResource(BaseResource):

    def __init__(self):
        self._controller = LocalidadesController()

    def get(self):
        return self._executar(
            lambda: self._controller.selecionar_todos(
                self._incluir_inativos()
            )
        )

    def post(self):
        return self._executar(
            lambda: self._controller.inserir(request.get_json(silent=True)),
            status=201,
        )


class LocalidadeResource(BaseResource):

    def __init__(self):
        self._controller = LocalidadesController()

    def get(self, id: int):
        return self._executar(
            lambda: self._controller.selecionar_por_id(id)
        )

    def put(self, id: int):
        return self._executar(
            lambda: self._controller.alterar(
                request.get_json(silent=True),
                id,
            )
        )

    def delete(self, id: int):
        return self._executar(
            lambda: self._controller.excluir(id),
            status=204,
        )


class RegistrosResource(BaseResource):

    def __init__(self):
        self._controller = RegistrosClimaticosController()

    def get(self):
        return self._executar(
            lambda: self._controller.selecionar_todos(
                self._incluir_inativos()
            )
        )

    def post(self):
        return self._executar(
            lambda: self._controller.inserir(request.get_json(silent=True)),
            status=201,
        )


class RegistroResource(BaseResource):

    def __init__(self):
        self._controller = RegistrosClimaticosController()

    def get(self, id: int):
        return self._executar(
            lambda: self._controller.selecionar_por_id(id)
        )

    def put(self, id: int):
        return self._executar(
            lambda: self._controller.alterar(
                request.get_json(silent=True),
                id,
            )
        )

    def delete(self, id: int):
        return self._executar(
            lambda: self._controller.excluir(id),
            status=204,
        )


class ThresholdsResource(BaseResource):

    def __init__(self):
        self._controller = ThresholdsController()

    def get(self):
        return self._executar(
            lambda: self._controller.selecionar_todos(
                self._incluir_inativos()
            )
        )

    def post(self):
        return self._executar(
            lambda: self._controller.inserir(request.get_json(silent=True)),
            status=201,
        )


class ThresholdResource(BaseResource):

    def __init__(self):
        self._controller = ThresholdsController()

    def get(self, id: int):
        return self._executar(
            lambda: self._controller.selecionar_por_id(id)
        )

    def put(self, id: int):
        return self._executar(
            lambda: self._controller.alterar(
                request.get_json(silent=True),
                id,
            )
        )

    def delete(self, id: int):
        return self._executar(
            lambda: self._controller.excluir(id),
            status=204,
        )


class HealthResource(Resource):

    def get(self):
        return {"status": "ok"}, 200
