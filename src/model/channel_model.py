import textwrap

from pydantic import AliasPath, BaseModel, ConfigDict, Field

class SnippetModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    titulo: str = Field(alias="title")
    descricao: str = Field(default="", alias="description")
    url_imagem: str = Field(alias="customUrl")
    data_publicacao: str = Field(alias="publishedAt")

    def __str__(self) -> str:
        linhas = [
            f"Título: {self.titulo}",
            f"Descrição: {self.descricao or '(sem descrição)'}",
            f"Handle/URL: {self.url_imagem}",
            f"Publicado em: {self.data_publicacao}",
        ]
        return "\n".join(linhas)


class PlaylistModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    uploads: str = Field(alias="uploads")

    def __str__(self) -> str:
        return f"uploads: {self.uploads}"


class ContentModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    playlist: PlaylistModel = Field(alias="relatedPlaylists")

    def __str__(self) -> str:
        return f"content: {self.playlist}"


class StatisticsModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    inscritos: int = Field(alias="subscriberCount")
    qtd_videos: int = Field(alias="videoCount")
    qtd_visualizacoes: int = Field(alias="viewCount")
    qtd_curtidas: int | None = Field(default=None, alias="likeCount")
    qtd_comentarios: int | None = Field(default=None, alias="commentCount")

    def __str__(self) -> str:
        linhas = [
            f"Inscritos: {self.inscritos}",
            f"Vídeos: {self.qtd_videos}",
            f"Visualizações: {self.qtd_visualizacoes}",
            f"Curtidas: {self.qtd_curtidas}",
            f"Comentários: {self.qtd_comentarios}",
        ]
        return "\n".join(linhas)


class BrandingModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    keywords: str = Field(validation_alias=AliasPath("channel", "keywords"))

    def __str__(self) -> str:
        return f"Keywords: {self.keywords}"


class ItemModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    canal_id: str = Field(alias="id")
    snippet: SnippetModel = Field(alias="snippet")
    content: ContentModel = Field(alias="contentDetails")
    statistics: StatisticsModel = Field(alias="statistics")
    branding: BrandingModel = Field(alias="brandingSettings")

    def __str__(self) -> str:
        linhas = [
            f"Canal ID: {self.canal_id}",
            textwrap.indent(str(self.snippet), "  "),
            textwrap.indent(str(self.content), "  "),
            textwrap.indent(str(self.statistics), "  "),
            textwrap.indent(str(self.branding), "  "),
        ]
        return "\n".join(linhas)

    
class ChannelModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    items: list[ItemModel] = Field(alias="items")

    def __str__(self) -> str:
        itens = "\n\n".join(textwrap.indent(str(item), "  ") for item in self.items)
        return f"Canal(is):\n{itens}"

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
