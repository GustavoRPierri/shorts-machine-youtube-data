from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentModel(BaseModel):
    # validate_by_name: também aceita os nomes em português (ex.: autor=...)
    model_config = ConfigDict(frozen=True, validate_by_name=True)

    id: str
    autor: str | None = Field(default=None, alias="author")
    autor_id: str | None = Field(default=None, alias="author_id")
    texto: str = Field(default="", alias="text")
    likes: int | None = Field(default=None, alias="like_count")
    data_postagem: datetime | None = Field(default=None, alias="timestamp")  # Unix epoch → datetime
    # "root" para comentário principal, ou o ID do comentário respondido.
    pai: str = Field(default="root", alias="parent")
    fixado: bool = Field(default=False, alias="is_pinned")
    favoritado: bool = Field(default=False, alias="is_favorited")
    autor_e_dono: bool = Field(default=False, alias="author_is_uploader")
    # O yt-dlp devolve os comentários numa lista plana; as respostas são
    # penduradas aqui por quem montar a árvore (ex.: o controller).
    respostas: list["CommentModel"] = Field(default_factory=list, alias="replies")
