from flask_restful import Api

from Routes.Resources import (
    HealthResource,
    LocalidadeResource,
    LocalidadesResource,
    RegistroResource,
    RegistrosResource,
    ThresholdResource,
    ThresholdsResource,
)


def registrar_recursos(app):
    api = Api(app)

    api.add_resource(HealthResource, "/health")

    api.add_resource(LocalidadesResource, "/localidades")
    api.add_resource(LocalidadeResource, "/localidades/<int:id>")

    api.add_resource(RegistrosResource, "/registros")
    api.add_resource(RegistroResource, "/registros/<int:id>")

    api.add_resource(ThresholdsResource, "/thresholds")
    api.add_resource(ThresholdResource, "/thresholds/<int:id>")

    return api
