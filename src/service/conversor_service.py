from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ConversorService:
    """Converte dicts brutos (API ou yt-dlp) para DTOs, de forma genérica.
    Quem decide a classe de destino é quem chama (a controller)."""
        
    def obter_dados(self, dados: dict, classe: type[T]) -> T:
        return classe.model_validate(dados)

    def obter_lista(self, dados: list[dict], classe: type[T]) -> list[T]:
        return [classe.model_validate(item) for item in dados]
