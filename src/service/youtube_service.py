import os
import re
import json
import math
import httpx
import logging
from typing import Iterator
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("api")

_BASE = "https://www.googleapis.com/youtube/v3"


class YoutubeService:

    def __init__(self, key: str, timeout: float = 30.0):
        self._key = key
        self._http = httpx.Client(base_url=_BASE, timeout=timeout)


    def get(self, endpoint: str, **params) -> dict:
        try:
            response = self._http.get(endpoint, params={**params, "key": self._key})
            response.raise_for_status()
            dados = response.json()

            log.info(
                f"[API][GET] search endpoint='{endpoint}'\n"
                f"{json.dumps(dados, indent=2, ensure_ascii=False)}"
            )

            return dados
        
        except Exception as ex:
            log.error(
                f"[API][GET] Erro ao buscar informacoes do endpoint {endpoint}: {ex}"
            )
            return False
        

    def paginate(self, endpoint: str, limite: int, **params) -> Iterator[dict]:
        try:
            pagina = 1
            total = 0
            while True:
                page = self.get(endpoint, **params)
                total += len(page.get("items", []))
                token = page.get("nextPageToken")
                page_info = page.get("pageInfo")
                total_paginas = math.ceil(page_info.get("totalResults") / page_info.get("resultsPerPage"))

                log.info(
                    f"[API][PAGINATE] endpoint='{endpoint}' pagina={pagina}/{total_paginas} itens={total} proximo_token={token}"
                )
                
                yield page

                if not token or (limite and total >= limite):
                    break
                pagina += 1
                params["pageToken"] = token

        except Exception as ex:
            log.error(
                f"[API][PAGINATE] Erro ao buscar informacoes do endpoint {endpoint}: {ex}"
            )
            return False

    def get_channel(self, canal_id: str) -> dict:
        """
        Retorna dict compatível com ChannelModel
        """
        params={"part": "snippet,contentDetails,statistics,brandingSettings"}
        params["forHandle"] = canal_id
        return self.get(endpoint="channels", **params)
        

    def search_videos(
        self, 
        canal_id: str,
        after: str = None,
        before: str = None,
        limite_por_pagina: int = None,
        max_paginas: int = None,
        video_duration: str = "any"
    ) -> list[dict]:
        try:
            
            params = {
                "part": "id",
                "channelId": canal_id,
                "type": "video",
                "order": "date",
                "videoDuration": video_duration,
                "publishedAfter": after or "1970-01-01T00:00:00Z",
                "publishedBefore": before or "2030-01-01T00:00:00Z",
                "maxResults": min(limite_por_pagina, 50) if limite_por_pagina else 50,
            }

            return self.paginate(endpoint="playlistItems", limite=max_paginas, **params)


        except Exception as ex:
            log.error(
                f"[API][SEARCH_VIDEOS] Erro ao buscar vídeos do canal {canal_id}: {ex}"
            )
            return False
    

    def get_videos(
        self,
        video_ids: list[str],
        limite: int = None,
        limite_por_pagina: int = None,
        max_paginas: int = None
    ) -> dict:
        """Retorna dict compatível com VideoModel (chaves em português).
        shortcut: busca apenas 1 página (max 50 itens); adicionar paginação quando limite > 50.
        """
        try:
            ids = video_ids[:limite] if limite else video_ids

            params = {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(ids),
                "maxResults": min(limite_por_pagina, 50) if limite_por_pagina else 50,
            }

            return self.paginate(endpoint="videos", limite=max_paginas, **params)

        except Exception as ex:
            log.error(
                f"[API][GET_VIDEOS] Erro ao buscar vídeos {video_ids}: {ex}"
            )
            return False


    def get_playlist(
        self,
        playlist_id: str,
        limite_por_pagina: int = None,
        max_paginas: int = None
    ) -> dict:
        """Retorna dict compatível com PlaylistModel: vídeos do canal via playlistItems.list,
        usando a playlist de uploads (1 unidade de cota, enumeração real — não busca aproximada).
        canal_id pode ser ID (UCxxxx) ou handle (@usuario).
        """
        try:
            params = {
                "part": "snippet,contentDetails",
                "playlistId": playlist_id,
                "maxResults": min(limite_por_pagina, 50) if limite_por_pagina else 5,
            }

            return self.paginate(endpoint="playlistItems", limite=max_paginas, **params)

        except Exception as ex:
            log.error(
                f"[API][GET_PLAYLIST] Erro ao buscar vídeos na playlist {playlist_id}: {ex}"
            )
            return False
