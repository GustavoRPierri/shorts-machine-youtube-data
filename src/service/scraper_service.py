import os
import json
import logging
import requests
import yt_dlp as ytdl
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("scraper")

class ScraperService():

    def __init__(self, end_proxy: str = None):
        self.end_proxy = end_proxy

    def get_comentarios(
        self, 
        video_url: str, 
        max_comentarios: int | None = None
    ) -> list[dict]:
        """
        Retorna lista plana de dicts no formato yt-dlp, compatível com CommentModel
        (aliases: author, text, like_count, timestamp, parent, is_pinned, ...).
        Nesting (respostas) deve ser feito pelo controller.
        """
        try:
            max_str = str(max_comentarios) if max_comentarios else "all"
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,   # fallback: legenda automática gerada pelo YouTube
                "getcomments": True,
                "extractor_args": {"youtube": {"max_comments": [max_str]}},
            }
            with ytdl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

            comentarios = info.get("comments")
            log.info(f"[SCRAPER][GET_COMENTARIOS] {len(comentarios)} comentários obtidos: {video_url}")
            return comentarios

        except Exception as ex:
            log.error(f"[SCRAPER][GET_COMENTARIOS] Erro ao buscar comentários {video_url}: {ex}")
            return False


    def get_transcricao(
        self,
        video_id: str,
        langs: list[str] = ["pt", "en"],
        tentativas: int = 5
    ) -> list[dict] | None:
        """
        Teste alternativo ao get_transcricao, usando a lib youtube-transcript-api
        em vez de yt-dlp. Retorna None se não houver legenda nos idiomas informados.
        """
        try:
            proxy_config = GenericProxyConfig(http_url=f"http://{self.end_proxy}", https_url=f"http://{self.end_proxy}") if self.end_proxy else None

            for tentativa in range(1, tentativas + 1):
                try:
                    api = YouTubeTranscriptApi(proxy_config=proxy_config)

                    if proxy_config:
                        ip_atual = requests.get("https://ipv4.webshare.io/", proxies=proxy_config.to_requests_dict(), timeout=10).text.strip()
                        log.info(f"[SCRAPER][GET_TRANSCRICAO_API] IP do proxy (tentativa {tentativa}/{tentativas}): {ip_atual}")

                    transcricao = api.fetch(video_id, languages=langs)
                    log.info(f"[SCRAPER][GET_TRANSCRICAO_API] Transcrição obtida: {video_id} (tentativa {tentativa}/{tentativas})")
                    return transcricao.to_raw_data()

                except Exception as ex_tentativa:
                    log.info(f"[SCRAPER][GET_TRANSCRICAO_API] IP bloqueado para {video_id}, tentativa {tentativa}/{tentativas}: {ex_tentativa}")

        except Exception as ex:
            log.error(f"[SCRAPER][GET_TRANSCRICAO_API] Erro ao buscar transcrição {video_id}: {ex}")
            return False

