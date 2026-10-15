from datetime import datetime, timedelta, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .comment_model import CommentModel


class VideoModel(BaseModel):
    # validate_by_name: também aceita os nomes em português (ex.: nome=...)
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    id: str
    url: str = Field(alias="url")
    nome: str = Field(alias="title")
    data_postagem: datetime = Field(alias="timestamp")
    duracao: timedelta = Field(alias="duration")          # segundos → timedelta
    descricao: str = Field(default="", alias="description")
    views: int = Field(alias="view_count")
    likes: int | None = Field(default=None, alias="like_count")
    deslikes: int | None = Field(default=None, alias="dislike_count")
    qtd_comentarios: int | None = Field(default=None, alias="comment_count")
    # Preenchidos pelo controller: árvore de comentários e transcrição (ou None).
    comentarios: list[CommentModel] = Field(default_factory=list, alias="comments")
    transcricao: dict | None = Field(default=None, alias="transcript")

    @model_validator(mode="before")
    @classmethod
    def ajustar_ytdlp(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        data = dict(data)  # cópia, para não alterar o dict original
        # Sem timestamp, cai para upload_date (AAAAMMDD).
        if data.get("timestamp") is None and data.get("upload_date"):
            data["timestamp"] = datetime.strptime(
                data["upload_date"], "%Y%m%d"
            ).replace(tzinfo=timezone.utc)
        # yt-dlp devolve None quando não há descrição.
        if data.get("description") is None:
            data.pop("description", None)
        return data
