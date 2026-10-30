import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import app


class TestInicializacaoAPI(unittest.TestCase):

    def test_app_importa(self):
        self.assertIsNotNone(app)

    def test_blueprints_registrados(self):
        blueprints = set(app.blueprints.keys())

        self.assertEqual(
            blueprints,
            {"localidades", "registros", "thresholds"},
        )

    def test_rotas_registradas(self):
        rotas = {}

        for regra in app.url_map.iter_rules():
            if regra.rule == "/static/<path:filename>":
                continue

            rotas.setdefault(regra.rule, set()).update(
                regra.methods - {"HEAD", "OPTIONS"}
            )

        self.assertEqual(
            set(rotas.keys()),
            {
                "/localidades",
                "/localidades/<int:id>",
                "/registros",
                "/registros/<int:id>",
                "/thresholds",
                "/thresholds/<int:id>",
            },
        )

        self.assertEqual(rotas["/localidades"], {"GET", "POST"})
        self.assertEqual(rotas["/localidades/<int:id>"], {"GET", "PUT", "DELETE"})
        self.assertEqual(rotas["/registros"], {"GET", "POST"})
        self.assertEqual(rotas["/registros/<int:id>"], {"GET", "PUT", "DELETE"})
        self.assertEqual(rotas["/thresholds"], {"GET", "POST"})
        self.assertEqual(rotas["/thresholds/<int:id>"], {"GET", "PUT", "DELETE"})

    def test_comando_init_db_registrado(self):
        self.assertIn("init-db", app.cli.commands)


if __name__ == "__main__":
    unittest.main()
