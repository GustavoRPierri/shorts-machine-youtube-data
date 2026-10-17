import textwrap

from pydantic import BaseModel, ConfigDict, Field, computed_field

class SnippetModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    titulo: str = Field(alias="title")
    descricao: str = Field(default="", alias="description")
    data_publicacao: str = Field(alias="publishedAt")
    canal_id: str = Field(alias="channelId")
    canal_nome: str = Field(alias="channelTitle")

    def __str__(self) -> str:
        linhas = [
            f"Título: {self.titulo}",
            f"Descrição: {self.descricao or '(sem descrição)'}",
            f"Publicado em: {self.data_publicacao}",
            f"Canal: {self.canal_nome} ({self.canal_id})",
        ]
        return "\n".join(linhas)


class StatisticsModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    qtd_visualizacoes: int = Field(alias="viewCount")
    qtd_curtidas: int | None = Field(default=None, alias="likeCount")
    qtd_comentarios: int | None = Field(default=None, alias="commentCount")

    def __str__(self) -> str:
        linhas = [
            f"Visualizações: {self.qtd_visualizacoes}",
            f"Curtidas: {self.qtd_curtidas}",
            f"Comentários: {self.qtd_comentarios}",
        ]
        return "\n".join(linhas)


class ContentDetailsModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    duracao: str = Field(alias="duration")

    def __str__(self) -> str:
        return f"Duração: {self.duracao}"


class ItemModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    video_id: str = Field(alias="id")
    snippet: SnippetModel = Field(alias="snippet")
    statistics: StatisticsModel = Field(alias="statistics")
    content_details: ContentDetailsModel = Field(alias="contentDetails")
    # Preenchidos pelo controller: árvore de comentários e transcrição (ou None).
    comentarios: list[dict] = Field(default_factory=list)
    transcricao: dict | None = Field(default=None)

    @computed_field
    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"

    def __str__(self) -> str:
        linhas = [
            f"Video ID: {self.video_id}",
            f"URL: {self.url}",
            textwrap.indent(str(self.snippet), "  "),
            textwrap.indent(str(self.statistics), "  "),
            textwrap.indent(str(self.content_details), "  "),
            f"  Comentários carregados: {len(self.comentarios)}",
            f"  Transcrição: {'disponível' if self.transcricao else 'indisponível'}",
        ]
        return "\n".join(linhas)


class VideoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    items: list[ItemModel] = Field(alias="items")

    def __str__(self) -> str:
        itens = "\n\n".join(textwrap.indent(str(item), "  ") for item in self.items)
        return f"Vídeo(s):\n{itens}"