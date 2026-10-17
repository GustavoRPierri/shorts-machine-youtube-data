import textwrap

from pydantic import BaseModel, ConfigDict, Field


class SnippetModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    titulo: str = Field(alias="title")
    descricao: str = Field(default="", alias="description")
    posicao: int = Field(alias="position")

    def __str__(self) -> str:
        linhas = [
            f"Título: {self.titulo}",
            f"Descrição: {self.descricao or '(sem descrição)'}",
            f"Posição: {self.posicao}",
        ]
        return "\n".join(linhas)


class ConteudoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    video_id: str = Field(alias="videoId")
    data_publicacao: str | None = Field(default=None, alias="videoPublishedAt")

    def __str__(self) -> str:
        return f"Video ID: {self.video_id} | Publicado em: {self.data_publicacao}"


class ItemModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    id_item: str = Field(alias="id")
    snippet: SnippetModel = Field(alias="snippet")
    conteudo: ConteudoModel = Field(alias="contentDetails")

    def __str__(self) -> str:
        linhas = [
            f"Item ID: {self.id_item}",
            textwrap.indent(str(self.snippet), "  "),
            textwrap.indent(str(self.conteudo), "  "),
        ]
        return "\n".join(linhas)


class PaginaInfoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    total_resultados: int = Field(alias="totalResults")
    resultados_por_pagina: int = Field(alias="resultsPerPage")

    def __str__(self) -> str:
        return f"Total de resultados: {self.total_resultados} | Por página: {self.resultados_por_pagina}"


class PlaylistModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    proxima_pagina: str | None = Field(default=None, alias="nextPageToken")
    pagina_info: PaginaInfoModel = Field(alias="pageInfo")
    items: list[ItemModel] = Field(default_factory=list, alias="items")

    def __str__(self) -> str:
        itens = "\n\n".join(textwrap.indent(str(item), "  ") for item in self.items)
        linhas = [
            f"Próxima página: {self.proxima_pagina}",
            f"Página info: {self.pagina_info}",
            "Itens:",
            itens,
        ]
        return "\n".join(linhas)
