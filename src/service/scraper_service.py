import json
import logging
import yt_dlp as ytdl
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("scraper")

class ScraperService():

    def __init__(self, url: str = None):
        self.video_url = url

    
    def get_transcricao(self, video_url: str, langs: list[str] = ["pt", "en"]) -> dict | None:
        """Retorna o json3 da primeira legenda disponível (manual > automática) nos idiomas
        informados, ou None se não houver. Alimenta VideoModel.transcricao."""
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,   # fallback: legenda automática gerada pelo YouTube
                "subtitleslangs": langs,
                "subtitlesformat": "json3",
                "socket_timeout": 10,
            }
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                # Tenta legendas manuais primeiro, depois automáticas
                for fonte in (info.get("subtitles") or {}, info.get("automatic_captions") or {}):
                    for lang in langs:
                        entradas = fonte.get(lang) or []
                        for entrada in entradas:
                            if entrada.get("ext") == "json3":
                                # Usa o cliente HTTP do próprio yt-dlp (headers/cookies corretos);
                                # requests puro leva 429 do YouTube nessa URL.
                                resp = ydl.urlopen(entrada["url"])
                                conteudo = resp.read()
                                log.info("[SCRAPER] Transcrição obtida: %s (%s)", video_url, lang)
                                return json.loads(conteudo)

            log.info("[SCRAPER][GET_TRANSCRICAO] Sem transcrição disponível: %s", video_url)
            return None

        except Exception as ex:
            log.error(f"[SCRAPER][GET_TRANSCRICAO] Erro ao buscar transcrição {video_url}: {ex}")
            return False


    def get_comentarios(self, video_url: str, max_comentarios: int | None = None) -> list[dict]:
        """Retorna lista plana de dicts no formato yt-dlp, compatível com CommentModel
        (aliases: author, text, like_count, timestamp, parent, is_pinned, ...).
        Nesting (respostas) deve ser feito pelo controller."""
        try:
            max_str = str(max_comentarios) if max_comentarios else "all"
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "getcomments": True,
                "extractor_args": {"youtube": {"max_comments": [max_str]}},
            }
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

            comentarios = info.get("comments") or []
            log.info("[SCRAPER][GET_COMENTARIOS] %d comentários obtidos: %s", len(comentarios), video_url)
            return comentarios

        except Exception as ex:
            log.error(f"[SCRAPER][GET_COMENTARIOS] Erro ao buscar comentários {video_url}: {ex}")
            return False
