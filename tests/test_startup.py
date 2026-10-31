import os
import unittest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import app


class TestInicializacaoAPI(unittest.TestCase):

    def test_app_importa(self):
        self.assertIsNotNone(app)

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
                "/health",
                "/localidades",
                "/localidades/<int:id>",
                "/registros",
                "/registros/<int:id>",
                "/thresholds",
                "/thresholds/<int:id>",
            },
        )

        self.assertEqual(rotas["/health"], {"GET"})
        self.assertEqual(rotas["/localidades"], {"GET", "POST"})
        self.assertEqual(rotas["/localidades/<int:id>"], {"GET", "PUT", "DELETE"})
        self.assertEqual(rotas["/registros"], {"GET", "POST"})
        self.assertEqual(rotas["/registros/<int:id>"], {"GET", "PUT", "DELETE"})
        self.assertEqual(rotas["/thresholds"], {"GET", "POST"})
        self.assertEqual(rotas["/thresholds/<int:id>"], {"GET", "PUT", "DELETE"})

    def test_comando_init_db_registrado(self):
        self.assertIn("init-db", app.cli.commands)

    def test_health(self):
        resposta = app.test_client().get("/health")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
