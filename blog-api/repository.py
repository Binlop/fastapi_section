from typing import Protocol, Any

class LaboratoryRepo(Protocol):

    async def get_available_laboratory(self) -> list[dict] | None:
        pass

class ProdLaboratoryRepo:
    async def get_available_laboratory(self) -> list[dict] | None:
        return {"id": 1, "name": "Лаборатория инструментальной геномики"}


class Stub:
    def __init__(self, dependency: Any):
        self._dependency = dependency

    def __call__(self):
        raise NotImplementedError(f"Забыли зарегистрировать реализацию для {self._dependency}")

    def __eq__(self, other):
        if isinstance(other, Stub):
            return self._dependency == other._dependency
        return NotImplemented

    def __hash__(self):
        return hash(self._dependency)