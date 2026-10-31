from abc import ABC

from Entity import db


class BaseRepository(ABC):
    """Repositório genérico com operações comuns de persistência."""

    def __init__(self, modelo):
        self._modelo = modelo
        self._nome_chave_primaria = list(
            modelo.__table__.primary_key.columns.keys()
        )[0]

    @property
    def modelo(self):
        return self._modelo

    @property
    def nome_chave_primaria(self) -> str:
        return self._nome_chave_primaria

    def selecionar_todos(self, incluir_inativos: bool = False):
        consulta = db.select(self._modelo)

        if hasattr(self._modelo, "Ativo") and not incluir_inativos:
            consulta = consulta.where(self._modelo.Ativo.is_(True))

        return db.session.execute(consulta).scalars().all()

    def buscar_por_id(self, id):
        return db.session.get(self._modelo, id)

    def inserir(self, entidade):
        db.session.add(entidade)
        db.session.commit()
        db.session.refresh(entidade)
        return entidade

    def inativar(self, id):
        entidade = self.buscar_por_id(id)

        if entidade is not None:
            entidade.Ativo = False
            db.session.commit()

        return entidade

    def existe_por_id(self, id: int) -> bool:
        coluna_id = getattr(self._modelo, self._nome_chave_primaria)

        return bool(
            db.session.execute(
                db.select(db.exists().where(coluna_id == id))
            ).scalar()
        )

    def existe_ativo_por_id(self, id: int) -> bool:
        coluna_id = getattr(self._modelo, self._nome_chave_primaria)
        condicoes = [coluna_id == id]

        if hasattr(self._modelo, "Ativo"):
            condicoes.append(self._modelo.Ativo.is_(True))

        return bool(
            db.session.execute(
                db.select(db.exists().where(*condicoes))
            ).scalar()
        )

    def alterar(self, entidade):
        db.session.commit()
        return entidade
