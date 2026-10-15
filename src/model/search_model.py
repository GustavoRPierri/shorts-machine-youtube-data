from pydantic import BaseModel, ConfigDict, Field

class IdModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    recurso_api: str = Field(alias="kind")
    video_id: str = Field(alias="videoId")

    def __str__(self) -> str:

        dados = {
            "recurso_api": self.recurso_api,
            "video_id": self.video_id,
        }

        return f"{dados}"

class ItemModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    recurso_api: str = Field(alias="kind")
    id_search: str = Field(alias="etag")
    id: IdModel = Field(alias="id")

    def __str__(self) -> str:

        dados = {
            "recurso_api": self.recurso_api,
            "id_search": self.id_search,
            "id": self.id
        }

        return f"{dados}"

class PaginaInfoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    total_resultados: int = Field(alias="totalResults")
    resultados_por_pagina: int = Field(alias="resultsPerPage")

    def __str__(self) -> str:

        dados = {
            "total_resultados": self.total_resultados,
            "resultados_por_pagina": self.resultados_por_pagina,
        }

        return f"{dados}"

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

        dados = {
            "recurso_api": self.recurso_api,
            "id_search": self.id_search,
            "proxima_pagina": self.proxima_pagina,
            "pagina_anterior": self.pagina_anterior,
            "codigo_regiao": self.codigo_regiao,
            "pagina_info": self.pagina_info,
            "items": self.items
        }

        return f"{dados}"
