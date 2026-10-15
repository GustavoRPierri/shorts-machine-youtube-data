import logging
import os
import re
from datetime import timedelta

import requests
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("api")

_BASE = "https://www.googleapis.com/youtube/v3"


class ApiService:
    """Acesso à YouTube Data API v3. Retorna dicts com chaves em português
    para alimentar diretamente os models via model_validate()."""

    def __init__(self):
        self._key = os.getenv("YOUTUBE_API_KEY")
        if not self._key:
            raise ValueError("YOUTUBE_API_KEY não definida no .env")

    @staticmethod
    def duracao_iso(iso: str) -> timedelta:
        """Converte duração ISO 8601 (PT1H2M3S) em timedelta."""
        horas = re.search(r"(\d+)H", iso)
        minutos = re.search(r"(\d+)M", iso)
        segundos = re.search(r"(\d+)S", iso)
        return timedelta(
            hours=int(horas.group(1)) if horas else 0,
            minutes=int(minutos.group(1)) if minutos else 0,
            seconds=int(segundos.group(1)) if segundos else 0,
        )

    # ── canal ─────────────────────────────────────────────────────────────────

    def get_channel(self, canal_id: str) -> dict:
        """Retorna dict compatível com ChannelModel (chaves em português).
        canal_id pode ser ID (UCxxxx) ou handle (@usuario).
        """
        params = {
            "part": "snippet,statistics,brandingSettings",
            # Campos retornados (economiza cota ao filtrar na API)
            "fields": (
                "items(id,"
                "snippet(title,description,customUrl,publishedAt,country,thumbnails),"
                "statistics(subscriberCount,videoCount,viewCount),"
                "brandingSettings(channel(keywords)))"
            ),
        }
        
        # handle começa com @; ID começa com UC
        if canal_id.startswith("@"):
            params["forHandle"] = canal_id
        else:
            params["id"] = canal_id
        params["key"] = self._key

        resposta = requests.get(f"{_BASE}/channels", params=params, timeout=15)
        resposta.raise_for_status() # Levanta HTTPError se status_code não for 2xx
        dados = resposta.json()

        log.info(f"[GET_CHANNEL] search {resposta.status_code}: {dados}")

        return dados
        
    def search_videos(
        self, 
        canal_id: str,
        after: str = None,
        before: str = None,
        limite: int = None
    ) -> list[dict]:
        try:
            # 1. Busca IDs dos vídeos via search.list
            max_resultados = min(limite, 50) if limite else 50

            params = {
                "part": "id",
                "channelId": canal_id,
                "type": "video",
                "order": "date",
                "publishedAfter": after or "1970-01-01T00:00:00Z",
                "publishedBefore": before or "2050-01-01T00:00:00Z",
                # "fields": "items(id/videoId)",
                "maxResults": max_resultados,
                "key": self._key,
            }
            resposta = requests.get(f"{_BASE}/search", params=params, timeout=15)
            resposta.raise_for_status()
            dados = resposta.json()

            log.info(f"[SEARCH_VIDEOS] search {resposta.status_code}: {dados}")

            return dados

        except Exception as ex:
            log.error(
                f"[SEARCH_VIDEOS] Erro ao buscar vídeos do canal {canal_id}: {ex}"
            )
            return False
    
    # ── vídeos ────────────────────────────────────────────────────────────────

    def get_videos(
        self, 
        video_id: str, 
        limite: int = None, 
    ) -> list[dict]:
        """Retorna lista de dicts compatíveis com VideoModel.
        shortcut: busca apenas 1 página (max 50 itens); adicionar paginação quando limite > 50.
        """

        # 2. Busca detalhes dos vídeos via videos.list
        params_videos = {
            "part": "snippet,statistics,contentDetails",
            "fields": (
                "items(id,"
                "snippet(title,description,publishedAt,channelId,channelTitle,tags,thumbnails),"
                "statistics(viewCount,likeCount,commentCount),"
                "contentDetails(duration,caption))"
            ),
        }
        params_videos["id"] = ",".join(ids)
        params_videos["key"] = self._key

        resp_videos = requests.get(f"{_BASE}/videos", params=params_videos, timeout=15)
        resp_videos.raise_for_status()
        dados_videos = resp_videos.json()
        log.info("[API] videos %s", resp_videos.status_code)

        # 3. Mapeia cada item para dict com chaves em português
        resultado = []
        for item in dados_videos.get("items") or []:
            vid_id = item["id"]
            snippet = item.get("snippet") or {}
            statistics = item.get("statistics") or {}
            content_details = item.get("contentDetails") or {}

            like_count = statistics.get("likeCount")
            comment_count = statistics.get("commentCount")
            duracao_iso = content_details.get("duration") or "PT0S"

            video = {
                "id": vid_id,
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "nome": snippet.get("title") or "",
                "data_postagem": snippet.get("publishedAt"),
                "duracao": self.duracao_iso(duracao_iso),
                "descricao": snippet.get("description") or "",
                "views": int(statistics.get("viewCount") or 0),
                "likes": int(like_count) if like_count else None,
                "qtd_comentarios": int(comment_count) if comment_count else None,
                "deslikes": None,  # API não expõe mais desde dez/2021
            }
            resultado.append(video)

        return dados_videos,resultado
