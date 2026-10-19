from pydantic import BaseModel, ConfigDict, Field


class TranscriptModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    texto: str = Field(alias="text")
    inicio: float = Field(alias="start")
    duracao: float = Field(alias="duration")

    def __str__(self) -> str:
        return f"[{self.inicio}s +{self.duracao}s] {self.texto}"
