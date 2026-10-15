from pydantic import BaseModel, ConfigDict, Field


class ChannelModel(BaseModel):
    # validate_by_name: também aceita os nomes em português (ex.: nome=...)
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    id: str = Field(alias="channel_id")                    # UCxxxx
    handle: str = Field(alias="uploader_id")               # @canal
    url: str = Field(alias="channel_url")
    nome: str = Field(alias="channel")
    descricao: str = Field(default="", alias="description")
    inscritos: int | None = Field(default=None, alias="channel_follower_count")
    verificado: bool = Field(default=False, alias="channel_is_verified")
    tags: list[str] = Field(default_factory=list)
    # O yt-dlp não fornece na página do canal; ficam None até virem de outra fonte.
    qtd_videos: int | None = Field(default=None, alias="video_count")
    qtd_visualizacoes: int | None = Field(default=None, alias="view_count")

    def __str__(self) -> str:

        dados = {
            "id": self.id,
            "handle": self.handle,
            "nome": self.nome,
            "descricao": self.descricao,
            "inscritos": self.inscritos,
            "verificado": self.verificado,
            "tags": self.tags,
            "qtd_videos": self.qtd_videos,
            "qtd_visualizacoes": self.qtd_visualizacoes,
        }

        return f"{dados}"


# itens = dados.get("items") or [] # Evita None caso items não exista
#         if not itens:
#             raise ValueError(f"Canal não encontrado: {canal_id}")

#         item = itens[0]
#         snippet = item.get("snippet") or {}
#         statistics = item.get("statistics") or {}
#         branding_channel = ((item.get("brandingSettings") or {}).get("channel") or {})
#         tags_bruto = branding_channel.get("keywords") or ""

#         inscritos = statistics.get("subscriberCount")
#         qtd_videos = statistics.get("videoCount")
#         qtd_visualizacoes = statistics.get("viewCount")

#         return {
#             "id": item["id"],
#             "handle": snippet.get("customUrl") or "",
#             "url": f"https://www.youtube.com/channel/{item['id']}",
#             "nome": snippet.get("title") or "",
#             "descricao": snippet.get("description") or "",
#             "inscritos": int(inscritos) if inscritos else None,
#             "qtd_videos": int(qtd_videos) if qtd_videos else None,
#             "qtd_visualizacoes": int(qtd_visualizacoes) if qtd_visualizacoes else None,
#             # tags vêm como string separada por espaço no brandingSettings
#             "tags": [t for t in tags_bruto.split() if t],
#         }
