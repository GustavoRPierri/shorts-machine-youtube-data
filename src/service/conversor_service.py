from datetime import timedelta
import logging
from typing import TypeVar

from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("conversor")

T = TypeVar("T", bound=BaseModel)

class ConversorService:
    """Converte dicts brutos (API ou yt-dlp) para DTOs, de forma genérica.
    Quem decide a classe de destino é quem chama (a controller)."""

    def obter_dados(self, dados: dict, classe: type[T]) -> T:
        try:
            dto = classe.model_validate(dados)
            log.info(f"[CONVERSOR][OBTER_DADOS] Dados convertidos para {classe.__name__}: {dto.__str__()}")
            return dto
        
        except Exception as ex:
            log.error(f"[CONVERSOR][OBTER_DADOS] Erro ao converter para {classe.__name__}: {ex}")
            return False

    def obter_lista(self, dados: list[dict], classe: type[T]) -> list[T]:
        try:
            dto_list = [self.obter_dados(item, classe) for item in dados]
            log.info(f"[CONVERSOR][OBTER_LISTA] Lista de dados convertidos para {classe.__name__}: {[dto.__str__() for dto in dto_list]}")
            return dto_list

        except Exception as ex:
            log.error(f"[CONVERSOR][OBTER_LISTA] Erro ao converter lista para {classe.__name__}: {ex}")
            return False
