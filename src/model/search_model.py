import textwrap

from pydantic import BaseModel, ConfigDict, Field

class IdModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    recurso_api: str = Field(alias="kind")
    video_id: str = Field(alias="videoId")

    def __str__(self) -> str:
        return f"Recurso: {self.recurso_api} | Video ID: {self.video_id}"

class ItemModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    recurso_api: str = Field(alias="kind")
    id_search: str = Field(alias="etag")
    id: IdModel = Field(alias="id")

    def __str__(self) -> str:
        linhas = [
            f"Recurso: {self.recurso_api}",
            f"Etag: {self.id_search}",
            f"  {self.id}",
        ]
        return "\n".join(linhas)

class PaginaInfoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    total_resultados: int = Field(alias="totalResults")
    resultados_por_pagina: int = Field(alias="resultsPerPage")

    def __str__(self) -> str:
        return f"Total de resultados: {self.total_resultados} | Por página: {self.resultados_por_pagina}"

class SearchModel(BaseModel):
    # validate_by_name: também aceita os nomes em português (ex.: nome=...)
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    recurso_api: str = Field(alias="kind")
    id_search: str = Field(alias="etag")
    proxima_pagina: str | None = Field(default=None, alias="nextPageToken")
    pagina_anterior: str | None = Field(default=None, alias="prevPageToken")
    codigo_regiao: str = Field(alias="regionCode")
    pagina_info: PaginaInfoModel = Field(alias="pageInfo")
    items: list[ItemModel] = Field(alias="items")

    def __str__(self) -> str:
        itens = "\n".join(textwrap.indent(str(item), "  ") for item in self.items)
        linhas = [
            f"Recurso: {self.recurso_api}",
            f"Etag: {self.id_search}",
            f"Região: {self.codigo_regiao}",
            f"Próxima página: {self.proxima_pagina}",
            f"Página anterior: {self.pagina_anterior}",
            f"Página info: {self.pagina_info}",
            "Itens:",
            itens,
        ]
        return "\n".join(linhas)
