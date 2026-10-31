import math
import random
from datetime import date, time, timedelta

from Entity import db
from Entity.Localidades import Localidades
from Entity.RegistrosClimaticos import RegistrosClimaticos
from Entity.Thresholds import Thresholds
from Enum.Estacao import Estacao
from Enum.Estado import Estado
from Enum.TipoLimiar import TipoLimiar
from Enum.Variavel import Variavel


LOCALIDADES_DEMO = (
    {
        "Nome": "Estação Centro",
        "Cidade": "São Paulo",
        "Estado": Estado.SP,
        "Latitude": -23.550520,
        "Longitude": -46.633308,
        "Offset": 0.0,
        "ChanceChuva": 0.25,
    },
    {
        "Nome": "Estação Litoral",
        "Cidade": "Santos",
        "Estado": Estado.SP,
        "Latitude": -23.960833,
        "Longitude": -46.333611,
        "Offset": 1.5,
        "ChanceChuva": 0.35,
    },
    {
        "Nome": "Estação Serra",
        "Cidade": "Campos do Jordão",
        "Estado": Estado.SP,
        "Latitude": -22.739444,
        "Longitude": -45.591389,
        "Offset": -4.0,
        "ChanceChuva": 0.30,
    },
)


def popular_dados_demo() -> dict:
    existente = db.session.execute(db.select(Localidades)).scalars().first()

    if existente is not None:
        return {
            "criado": False,
            "mensagem": "O banco já possui localidades; seed não executado.",
        }

    localidades = []

    for dados in LOCALIDADES_DEMO:
        localidades.append(
            Localidades(
                Nome=dados["Nome"],
                Cidade=dados["Cidade"],
                Estado=dados["Estado"],
                Latitude=dados["Latitude"],
                Longitude=dados["Longitude"],
                Ativo=True,
            )
        )

    db.session.add_all(localidades)
    db.session.commit()

    registros = []
    inicio = date(2025, 1, 1)
    total_dias = 365

    for indice, (localidade, dados) in enumerate(
        zip(localidades, LOCALIDADES_DEMO),
        start=1,
    ):
        gerador = random.Random(42 + indice * 1000)

        for numero_dia in range(total_dias):
            dia = inicio + timedelta(days=numero_dia)
            ciclo = math.cos(
                (dia.timetuple().tm_yday - 15) * 2 * math.pi / 365
            )
            media_base = 22.0 + 4.0 * ciclo + dados["Offset"]
            temp_max = media_base + 5.0 + gerador.uniform(-1.0, 1.0)
            temp_min = media_base - 5.0 + gerador.uniform(-1.0, 1.0)
            temp_media = (temp_max + temp_min) / 2.0
            umidade = 70.0 - 10.0 * ciclo + gerador.uniform(-5.0, 5.0)
            umidade = min(100.0, max(20.0, umidade))

            estiagem_centro = (
                indice == 1
                and date(2025, 8, 1) <= dia <= date(2025, 8, 20)
            )

            if estiagem_centro:
                precipitacao = 0.0
            elif gerador.random() < dados["ChanceChuva"]:
                precipitacao = round(gerador.uniform(1.0, 35.0), 2)
            else:
                precipitacao = 0.0

            velocidade_vento = round(gerador.uniform(2.0, 15.0), 2)
            pressao = round(
                1013.0 + 4.0 * ciclo + gerador.uniform(-3.0, 3.0),
                2,
            )

            registros.append(
                RegistrosClimaticos(
                    TempMax=round(temp_max, 1),
                    TempMin=round(temp_min, 1),
                    TempMedia=round(temp_media, 1),
                    UmidadeRelativa=round(umidade, 2),
                    Precipitacao=precipitacao,
                    VelocidadeVento=velocidade_vento,
                    PressaoAtmosferica=pressao,
                    Data=dia,
                    Hora=time(12, 0, 0),
                    Ativo=True,
                    FKLocalidade=localidade.IDLocalidade,
                )
            )

    db.session.add_all(registros)

    thresholds = []

    for localidade in localidades:
        definicoes = (
            (Variavel.TEMPERATURA, TipoLimiar.MAXIMO, Estacao.VERAO, 31.5),
            (Variavel.TEMPERATURA, TipoLimiar.MINIMO, Estacao.INVERNO, 13.5),
            (Variavel.PRECIPITACAO, TipoLimiar.MAXIMO, Estacao.ANUAL, 34.0),
            (Variavel.PRECIPITACAO, TipoLimiar.DIASSEMCHUVA, Estacao.ANUAL, 15.0),
            (Variavel.UMIDADE, TipoLimiar.MINIMO, Estacao.ANUAL, 57.0),
            (Variavel.VELOCIDADEVENTO, TipoLimiar.MAXIMO, Estacao.ANUAL, 14.0),
        )

        for variavel, tipo, estacao, valor in definicoes:
            thresholds.append(
                Thresholds(
                    FKLocalidade=localidade.IDLocalidade,
                    Variavel=variavel,
                    TipoLimiar=tipo,
                    EstacaoDoAno=estacao,
                    Valor=valor,
                    Ativo=True,
                )
            )

    db.session.add_all(thresholds)
    db.session.commit()

    return {
        "criado": True,
        "localidades": len(localidades),
        "registros": len(registros),
        "thresholds": len(thresholds),
        "mensagem": "Dados de demonstração criados com sucesso.",
    }
