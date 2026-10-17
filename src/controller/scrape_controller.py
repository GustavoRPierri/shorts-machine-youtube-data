from logging import log

from service import ApiService, ScraperService, ConversorService
from model import ChannelModel, VideoModel, CommentModel

api = ApiService()
scraper = ScraperService()
conversor = ConversorService()

@staticmethod
def duracao_iso(iso: str) -> timedelta:
    """Converte duração ISO 8601 (PT1H2M3S) em timedelta."""
    try:
        horas = re.search(r"(\d+)H", iso)
        minutos = re.search(r"(\d+)M", iso)
        segundos = re.search(r"(\d+)S", iso)
        
        return timedelta(
            hours=int(horas.group(1)) if horas else 0,
            minutes=int(minutos.group(1)) if minutos else 0,
            seconds=int(segundos.group(1)) if segundos else 0,
        )
    
    except Exception as ex:
        log.error(
            f"[API][DURACAO_ISO] Erro ao converter duração ISO {iso}: {ex}"
        )
        return False

