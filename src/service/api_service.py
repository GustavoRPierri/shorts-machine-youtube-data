import logging
import os
import re
from datetime import datetime, timedelta, timezone

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

    # ── canal ─────────────────────────────────────────────────────────────────

    def get_channel(self, canal_id: str) -> dict:
        """Retorna dict compatível com ChannelModel (chaves em português).
        canal_id pode ser ID (UCxxxx) ou handle (@usuario).
        """
        try:
            params = {
                "part": "snippet,statistics,brandingSettings",
                # Campos retornados (economiza cota ao filtrar na API)
                "fields": (
                    "items(id,"
                    "snippet(title,description,customUrl,publishedAt,country,thumbnails),"
                    "contentDetails(relatedPlaylists(uploads)),"
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

            log.info(f"[API][GET_CHANNEL] search {resposta.status_code}: {dados}")

            return dados
        
        except Exception as ex:
            log.error(
                f"[API][GET_CHANNEL] Erro ao buscar informacoes do canal {canal_id}: {ex}"
            )
            return False

    def search_videos(
        self, 
        canal_id: str,
        after: str = None,
        before: str = None,
        limite: int = None,
        video_duration: str = "any"
    ) -> list[dict]:
        try:
            # 1. Busca IDs dos vídeos via search.list
            max_resultados = min(limite, 50) if limite else 50

            params = {
                "part": "id",
                "channelId": canal_id,
                "type": "video",
                "order": "date",
                "videoDuration": video_duration,
                "publishedAfter": after or "1970-01-01T00:00:00Z",
                "publishedBefore": before or "2030-01-01T00:00:00Z",
                # "fields": "items(id/videoId)",
                "maxResults": max_resultados,
                "key": self._key,
            }
            
            resposta = requests.get(f"{_BASE}/search", params=params, timeout=15)
            resposta.raise_for_status()
            dados = resposta.json()

            log.info(f"[API][SEARCH_VIDEOS] search {resposta.status_code}: {dados}")

            return dados

        except Exception as ex:
            log.error(
                f"[API][SEARCH_VIDEOS] Erro ao buscar vídeos do canal {canal_id}: {ex}"
            )
            return False
    
    # ── vídeos ────────────────────────────────────────────────────────────────

    def get_videos(
        self,
        video_ids: list[str],
        limite: int = None,
    ) -> dict:
        """Retorna dict compatível com VideoModel (chaves em português).
        shortcut: busca apenas 1 página (max 50 itens); adicionar paginação quando limite > 50.
        """
        try:
            ids = video_ids[:limite] if limite else video_ids

            params = {
                "part": "snippet,statistics,contentDetails",
                "fields": (
                    "items(id,"
                    "snippet(title,description,publishedAt,channelId,channelTitle),"
                    "statistics(viewCount,likeCount,commentCount),"
                    "contentDetails(duration))"
                ),
                "id": ",".join(ids),
                "key": self._key,
            }

            resposta = requests.get(f"{_BASE}/videos", params=params, timeout=15)
            resposta.raise_for_status()
            dados = resposta.json()

            log.info(f"[API][GET_VIDEOS] search {resposta.status_code}: {dados}")

            return dados

        except Exception as ex:
            log.error(
                f"[API][GET_VIDEOS] Erro ao buscar vídeos {video_ids}: {ex}"
            )
            return False

    def get_playlist(
        self, 
        playlist_id: str, 
        limite: int = None,
        page_token: str = None
    ) -> dict:
        """Retorna dict compatível com PlaylistModel: vídeos do canal via playlistItems.list,
        usando a playlist de uploads (1 unidade de cota, enumeração real — não busca aproximada).
        canal_id pode ser ID (UCxxxx) ou handle (@usuario).
        """
        try:

            params = {
                "part": "snippet,contentDetails",
                "fields": (
                    "items(id,"
                    "snippet(title,description,position),"
                    "contentDetails(videoId,videoPublishedAt)),"
                    "nextPageToken,pageInfo"
                ),
                "playlistId": playlist_id,
                "maxResults": min(limite, 50) if limite else 50,
                "key": self._key,
            }

            if page_token:
                params["pageToken"] = page_token

            resposta = requests.get(f"{_BASE}/playlistItems", params=params, timeout=15)
            resposta.raise_for_status()
            dados = resposta.json()

            log.info(f"[API][GET_PLAYLIST] search {resposta.status_code}: {dados}")

            return dados

        except Exception as ex:
            log.error(
                f"[API][GET_PLAYLIST] Erro ao buscar vídeos na playlist {playlist_id}: {ex}"
            )
            return False
