import csv
import io
import statistics
from datetime import date

from Enum.Estacao import Estacao
from Enum.TipoLimiar import TipoLimiar
from Enum.Variavel import Variavel
from Exception.exception import ElementoNaoEncontradoException
from Repository.LocalidadesRepository import LocalidadesRepository
from Repository.RegistrosClimaticosRepository import (
    RegistrosClimaticosRepository,
)
from Repository.ThresholdsRepository import ThresholdsRepository


CAMPOS_CLIMATICOS = (
    ("TempMax", "Temperatura máxima"),
    ("TempMin", "Temperatura mínima"),
    ("TempMedia", "Temperatura média"),
    ("UmidadeRelativa", "Umidade relativa"),
    ("Precipitacao", "Precipitação"),
    ("VelocidadeVento", "Velocidade do vento"),
    ("PressaoAtmosferica", "Pressão atmosférica"),
)

CAMPOS_POR_VARIAVEL = {
    Variavel.UMIDADE: "UmidadeRelativa",
    Variavel.PRECIPITACAO: "Precipitacao",
    Variavel.VELOCIDADEVENTO: "VelocidadeVento",
    Variavel.PRESSAOATMOSFERICA: "PressaoAtmosferica",
}

NOMES_MESES = (
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)

ESTACOES_SUL = (
    (Estacao.VERAO, "Verão"),
    (Estacao.OUTONO, "Outono"),
    (Estacao.INVERNO, "Inverno"),
    (Estacao.PRIMAVERA, "Primavera"),
)

TIPOS_EXPORTACAO = {
    "registros",
    "estatisticas",
    "comparacao",
    "eventos",
    "sazonalidade",
}


class AnaliseService:
    """Regras de consulta, análise, eventos extremos e exportação."""

    def __init__(self):
        self._registros_repositorio = RegistrosClimaticosRepository()
        self._localidades_repositorio = LocalidadesRepository()
        self._thresholds_repositorio = ThresholdsRepository()

    @property
    def registros_repositorio(self):
        return self._registros_repositorio

    @property
    def localidades_repositorio(self):
        return self._localidades_repositorio

    @property
    def thresholds_repositorio(self):
        return self._thresholds_repositorio

    def estatisticas(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ) -> dict:
        registros = self._obter_registros(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )
        localidade = self._obter_localidade(localidade_id)

        return {
            "IDLocalidade": localidade_id,
            "Nome": localidade.Nome if localidade else "Todas as localidades",
            "DataInicio": self._data_iso(data_inicio),
            "DataFim": self._data_iso(data_fim),
            "QuantidadeRegistros": len(registros),
            "Estatisticas": self._calcular_estatisticas(registros),
        }

    def comparar(
        self,
        data_inicio,
        data_fim,
        localidade_ids: list[int],
    ) -> dict:
        ids = list(dict.fromkeys(localidade_ids))

        if len(ids) < 2:
            raise ValueError(
                "Informe pelo menos duas localidades para a comparação."
            )

        for localidade_id in ids:
            self._obter_localidade(localidade_id)

        self._validar_periodo(data_inicio, data_fim)

        localidades = []

        for localidade_id in ids:
            localidade = self._obter_localidade(localidade_id)
            registros = self._obter_registros(
                data_inicio=data_inicio,
                data_fim=data_fim,
                localidade_id=localidade_id,
            )

            localidades.append(
                {
                    "IDLocalidade": localidade.IDLocalidade,
                    "Nome": localidade.Nome,
                    "Cidade": localidade.Cidade,
                    "Estado": localidade.Estado.value,
                    "QuantidadeRegistros": len(registros),
                    "Estatisticas": self._calcular_estatisticas(registros),
                }
            )

        return {
            "DataInicio": self._data_iso(data_inicio),
            "DataFim": self._data_iso(data_fim),
            "Localidades": localidades,
        }

    def eventos_extremos(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ) -> dict:
        localidade = self._obter_localidade(localidade_id)

        if localidade is None:
            raise ValueError(
                "Informe a localidade para consultar eventos extremos."
            )

        registros = self._obter_registros(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )
        thresholds = self._thresholds_repositorio.selecionar_por_localidade(
            localidade_id
        )

        eventos = []

        for threshold in thresholds:
            if threshold.TipoLimiar == TipoLimiar.DIASSEMCHUVA:
                eventos.extend(
                    self._eventos_dias_sem_chuva(
                        registros,
                        threshold,
                        localidade,
                    )
                )
                continue

            eventos.extend(
                self._eventos_limiar(
                    registros,
                    threshold,
                    localidade,
                )
            )

        eventos.sort(
            key=lambda evento: (
                evento.get("Data") or evento.get("DataInicio") or "",
                evento.get("Hora") or "",
            )
        )

        resultado = {
            "IDLocalidade": localidade.IDLocalidade,
            "Nome": localidade.Nome,
            "DataInicio": self._data_iso(data_inicio),
            "DataFim": self._data_iso(data_fim),
            "QuantidadeEventos": len(eventos),
            "Eventos": eventos,
        }

        if not thresholds:
            resultado["Aviso"] = (
                "Nenhum threshold ativo cadastrado para esta localidade."
            )

        return resultado

    def sazonalidade(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
        agrupamento: str = "mes",
    ) -> dict:
        if agrupamento not in {"mes", "estacao"}:
            raise ValueError(
                "O agrupamento deve ser 'mes' ou 'estacao'."
            )

        localidade = self._obter_localidade(localidade_id)
        registros = self._obter_registros(
            data_inicio=data_inicio,
            data_fim=data_fim,
            localidade_id=localidade_id,
        )

        grupos = []

        if agrupamento == "mes":
            for numero, nome in enumerate(NOMES_MESES, start=1):
                registros_mes = [
                    registro
                    for registro in registros
                    if registro.Data.month == numero
                ]
                grupos.append(
                    {
                        "Chave": numero,
                        "Grupo": nome,
                        "Quantidade": len(registros_mes),
                        "Medias": self._calcular_medias(registros_mes),
                    }
                )
        else:
            for estacao, nome in ESTACOES_SUL:
                registros_estacao = [
                    registro
                    for registro in registros
                    if self._estacao(registro.Data) == estacao
                ]
                grupos.append(
                    {
                        "Chave": estacao.value,
                        "Grupo": nome,
                        "Quantidade": len(registros_estacao),
                        "Medias": self._calcular_medias(registros_estacao),
                    }
                )

        return {
            "IDLocalidade": localidade_id,
            "Nome": localidade.Nome if localidade else "Todas as localidades",
            "DataInicio": self._data_iso(data_inicio),
            "DataFim": self._data_iso(data_fim),
            "Agrupamento": agrupamento,
            "Grupos": grupos,
        }

    def exportar(
        self,
        tipo: str,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
        localidade_ids: list[int] | None = None,
        agrupamento: str = "mes",
    ) -> tuple[str, str]:
        if tipo not in TIPOS_EXPORTACAO:
            raise ValueError(
                "Tipo de exportação inválido. Use registros, estatisticas, "
                "comparacao, eventos ou sazonalidade."
            )

        localidade_ids = localidade_ids or []

        if tipo == "registros":
            campos, linhas = self._linhas_registros(
                data_inicio,
                data_fim,
                localidade_id,
            )
        elif tipo == "estatisticas":
            campos, linhas = self._linhas_estatisticas(
                data_inicio,
                data_fim,
                localidade_id,
            )
        elif tipo == "comparacao":
            campos, linhas = self._linhas_comparacao(
                data_inicio,
                data_fim,
                localidade_ids,
            )
        elif tipo == "eventos":
            campos, linhas = self._linhas_eventos(
                data_inicio,
                data_fim,
                localidade_id,
            )
        else:
            campos, linhas = self._linhas_sazonalidade(
                data_inicio,
                data_fim,
                localidade_id,
                agrupamento,
            )

        nome_arquivo = f"{tipo}_{date.today().isoformat()}.csv"

        return nome_arquivo, self._gerar_csv(campos, linhas)

    def _obter_registros(
        self,
        data_inicio=None,
        data_fim=None,
        localidade_id: int | None = None,
    ):
        self._validar_periodo(data_inicio, data_fim)
        localidade = self._obter_localidade(localidade_id)

        if localidade_id is not None and localidade is None:
            raise ElementoNaoEncontradoException(
                f"Localidade com o id: {localidade_id} não foi encontrada!"
            )

        return self._registros_repositorio.selecionar_por_filtros(
            data_inicio=data_inicio,
            data_fim=data_fim,
            fk_localidade=localidade_id,
            incluir_inativos=False,
        )

    def _obter_localidade(self, localidade_id: int | None):
        if localidade_id is None:
            return None

        return self._localidades_repositorio.buscar_por_id(localidade_id)

    def _validar_periodo(self, data_inicio=None, data_fim=None):
        if (
            data_inicio is not None
            and data_fim is not None
            and data_inicio > data_fim
        ):
            raise ValueError(
                "A data inicial não pode ser posterior à data final!"
            )

    def _calcular_estatisticas(self, registros) -> list[dict]:
        resultado = []

        for campo, descricao in CAMPOS_CLIMATICOS:
            valores = [
                float(getattr(registro, campo))
                for registro in registros
                if getattr(registro, campo) is not None
            ]

            if not valores:
                continue

            resultado.append(
                {
                    "Variavel": campo,
                    "Descricao": descricao,
                    "Media": round(statistics.mean(valores), 2),
                    "Mediana": round(statistics.median(valores), 2),
                    "Maximo": round(max(valores), 2),
                    "Minimo": round(min(valores), 2),
                    "Quantidade": len(valores),
                }
            )

        return resultado

    def _calcular_medias(self, registros) -> dict:
        medias = {}

        for campo, _ in CAMPOS_CLIMATICOS:
            valores = [
                float(getattr(registro, campo))
                for registro in registros
                if getattr(registro, campo) is not None
            ]

            medias[campo] = (
                round(statistics.mean(valores), 2) if valores else None
            )

        return medias

    def _eventos_limiar(self, registros, threshold, localidade) -> list[dict]:
        campo = self._campo_do_limiar(threshold)
        eventos = []

        for registro in registros:
            if not self._registro_na_estacao(registro, threshold):
                continue

            valor = float(getattr(registro, campo))
            limiar = float(threshold.Valor)
            ocorreu = (
                threshold.TipoLimiar == TipoLimiar.MAXIMO
                and valor >= limiar
            ) or (
                threshold.TipoLimiar == TipoLimiar.MINIMO
                and valor <= limiar
            )

            if not ocorreu:
                continue

            eventos.append(
                {
                    "IDThreshold": threshold.IDThreshold,
                    "Variavel": threshold.Variavel.value,
                    "TipoLimiar": threshold.TipoLimiar.value,
                    "EstacaoDoAno": threshold.EstacaoDoAno.value,
                    "Limiar": limiar,
                    "Valor": round(valor, 2),
                    "Data": registro.Data.isoformat(),
                    "Hora": registro.Hora.isoformat(),
                    "Descricao": (
                        f"{threshold.Variavel.value} {threshold.TipoLimiar.value} "
                        f"em {localidade.Nome}: {valor:.2f} "
                        f"(limiar {limiar:.2f}) em {registro.Data.isoformat()}."
                    ),
                }
            )

        return eventos

    def _eventos_dias_sem_chuva(
        self,
        registros,
        threshold,
        localidade,
    ) -> list[dict]:
        registros_estacao = [
            registro
            for registro in registros
            if self._registro_na_estacao(registro, threshold)
        ]
        precipitacao_por_dia = {}

        for registro in registros_estacao:
            dia = registro.Data
            precipitacao_por_dia[dia] = (
                precipitacao_por_dia.get(dia, 0.0)
                + float(registro.Precipitacao)
            )

        limiar_dias = int(float(threshold.Valor))
        eventos = []
        inicio = None
        dias = 0
        dia_anterior = None

        for dia in sorted(precipitacao_por_dia):
            seco = precipitacao_por_dia[dia] <= 0.01
            consecutivo = (
                dia_anterior is not None
                and (dia - dia_anterior).days == 1
            )

            if seco and (inicio is None or consecutivo):
                if inicio is None:
                    inicio = dia
                    dias = 0
                dias += 1
            else:
                if inicio is not None and dias >= limiar_dias:
                    eventos.append(
                        self._evento_seca(
                            threshold,
                            localidade,
                            inicio,
                            dia_anterior,
                            dias,
                        )
                    )

                if seco:
                    inicio = dia
                    dias = 1
                else:
                    inicio = None
                    dias = 0

            dia_anterior = dia

        if inicio is not None and dias >= limiar_dias:
            eventos.append(
                self._evento_seca(
                    threshold,
                    localidade,
                    inicio,
                    dia_anterior,
                    dias,
                )
            )

        return eventos

    def _evento_seca(
        self,
        threshold,
        localidade,
        inicio,
        fim,
        dias,
    ) -> dict:
        return {
            "IDThreshold": threshold.IDThreshold,
            "Variavel": threshold.Variavel.value,
            "TipoLimiar": threshold.TipoLimiar.value,
            "EstacaoDoAno": threshold.EstacaoDoAno.value,
            "Limiar": float(threshold.Valor),
            "DataInicio": inicio.isoformat(),
            "DataFim": fim.isoformat(),
            "Dias": dias,
            "Descricao": (
                f"{dias} dias consecutivos sem chuva em {localidade.Nome} "
                f"({inicio.isoformat()} a {fim.isoformat()})."
            ),
        }

    def _campo_do_limiar(self, threshold) -> str:
        if threshold.Variavel == Variavel.TEMPERATURA:
            if threshold.TipoLimiar == TipoLimiar.MAXIMO:
                return "TempMax"
            return "TempMin"

        return CAMPOS_POR_VARIAVEL[threshold.Variavel]

    def _registro_na_estacao(self, registro, threshold) -> bool:
        return (
            threshold.EstacaoDoAno == Estacao.ANUAL
            or self._estacao(registro.Data) == threshold.EstacaoDoAno
        )

    @staticmethod
    def _estacao(dia: date) -> Estacao:
        mes = dia.month

        if mes in (12, 1, 2):
            return Estacao.VERAO
        if mes in (3, 4, 5):
            return Estacao.OUTONO
        if mes in (6, 7, 8):
            return Estacao.INVERNO
        return Estacao.PRIMAVERA

    @staticmethod
    def _data_iso(dia):
        return dia.isoformat() if dia is not None else None

    def _linhas_registros(
        self,
        data_inicio,
        data_fim,
        localidade_id,
    ):
        registros = self._obter_registros(
            data_inicio,
            data_fim,
            localidade_id,
        )
        campos = (
            "IDRegistrosClimaticos",
            "FKLocalidade",
            "Data",
            "Hora",
            "TempMax",
            "TempMin",
            "TempMedia",
            "UmidadeRelativa",
            "Precipitacao",
            "VelocidadeVento",
            "PressaoAtmosferica",
            "Ativo",
        )
        linhas = [
            {
                "IDRegistrosClimaticos": registro.IDRegistrosClimaticos,
                "FKLocalidade": registro.FKLocalidade,
                "Data": registro.Data.isoformat(),
                "Hora": registro.Hora.isoformat(),
                "TempMax": float(registro.TempMax),
                "TempMin": float(registro.TempMin),
                "TempMedia": float(registro.TempMedia),
                "UmidadeRelativa": float(registro.UmidadeRelativa),
                "Precipitacao": float(registro.Precipitacao),
                "VelocidadeVento": float(registro.VelocidadeVento),
                "PressaoAtmosferica": float(registro.PressaoAtmosferica),
                "Ativo": registro.Ativo,
            }
            for registro in registros
        ]

        return campos, linhas

    def _linhas_estatisticas(
        self,
        data_inicio,
        data_fim,
        localidade_id,
    ):
        resultado = self.estatisticas(
            data_inicio,
            data_fim,
            localidade_id,
        )
        campos = (
            "IDLocalidade",
            "Nome",
            "DataInicio",
            "DataFim",
            "Variavel",
            "Descricao",
            "Media",
            "Mediana",
            "Maximo",
            "Minimo",
            "Quantidade",
        )
        linhas = [
            {
                "IDLocalidade": resultado["IDLocalidade"],
                "Nome": resultado["Nome"],
                "DataInicio": resultado["DataInicio"],
                "DataFim": resultado["DataFim"],
                **estatistica,
            }
            for estatistica in resultado["Estatisticas"]
        ]

        return campos, linhas

    def _linhas_comparacao(
        self,
        data_inicio,
        data_fim,
        localidade_ids,
    ):
        resultado = self.comparar(
            data_inicio,
            data_fim,
            localidade_ids,
        )
        campos = (
            "IDLocalidade",
            "Nome",
            "Cidade",
            "Estado",
            "DataInicio",
            "DataFim",
            "Variavel",
            "Descricao",
            "Media",
            "Mediana",
            "Maximo",
            "Minimo",
            "Quantidade",
        )
        linhas = []

        for localidade in resultado["Localidades"]:
            for estatistica in localidade["Estatisticas"]:
                linhas.append(
                    {
                        "IDLocalidade": localidade["IDLocalidade"],
                        "Nome": localidade["Nome"],
                        "Cidade": localidade["Cidade"],
                        "Estado": localidade["Estado"],
                        "DataInicio": resultado["DataInicio"],
                        "DataFim": resultado["DataFim"],
                        **estatistica,
                    }
                )

        return campos, linhas

    def _linhas_eventos(
        self,
        data_inicio,
        data_fim,
        localidade_id,
    ):
        resultado = self.eventos_extremos(
            data_inicio,
            data_fim,
            localidade_id,
        )
        campos = (
            "IDThreshold",
            "Variavel",
            "TipoLimiar",
            "EstacaoDoAno",
            "Limiar",
            "Valor",
            "Data",
            "Hora",
            "DataInicio",
            "DataFim",
            "Dias",
            "Descricao",
        )
        linhas = [
            {campo: evento.get(campo, "") for campo in campos}
            for evento in resultado["Eventos"]
        ]

        return campos, linhas

    def _linhas_sazonalidade(
        self,
        data_inicio,
        data_fim,
        localidade_id,
        agrupamento,
    ):
        resultado = self.sazonalidade(
            data_inicio,
            data_fim,
            localidade_id,
            agrupamento,
        )
        campos = (
            "IDLocalidade",
            "Nome",
            "Agrupamento",
            "Chave",
            "Grupo",
            "Quantidade",
            *[campo for campo, _ in CAMPOS_CLIMATICOS],
        )
        linhas = []

        for grupo in resultado["Grupos"]:
            linhas.append(
                {
                    "IDLocalidade": resultado["IDLocalidade"],
                    "Nome": resultado["Nome"],
                    "Agrupamento": resultado["Agrupamento"],
                    "Chave": grupo["Chave"],
                    "Grupo": grupo["Grupo"],
                    "Quantidade": grupo["Quantidade"],
                    **grupo["Medias"],
                }
            )

        return campos, linhas

    @staticmethod
    def _gerar_csv(campos, linhas) -> str:
        buffer = io.StringIO()
        buffer.write("\ufeff")
        escritor = csv.DictWriter(
            buffer,
            fieldnames=campos,
            delimiter=";",
            extrasaction="ignore",
        )
        escritor.writeheader()
        escritor.writerows(linhas)

        return buffer.getvalue()
