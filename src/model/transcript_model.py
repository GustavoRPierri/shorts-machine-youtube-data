import textwrap

from pydantic import BaseModel, ConfigDict, Field


class SegModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    texto: str = Field(default="", alias="utf8")

    def __str__(self) -> str:
        return self.texto


class SegmentoModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    inicio_ms: int = Field(alias="tStartMs")
    duracao_ms: int = Field(default=0, alias="dDurationMs")
    segs: list[SegModel] = Field(default_factory=list, alias="segs")

    def __str__(self) -> str:
        texto = "".join(str(seg) for seg in self.segs)
        return f"[{self.inicio_ms}ms +{self.duracao_ms}ms] {texto}"


class TranscriptModel(BaseModel):
    model_config = ConfigDict(frozen=True, validate_by_name=True, extra="ignore")

    segmentos: list[SegmentoModel] = Field(default_factory=list, alias="events")

    def __str__(self) -> str:
        linhas = "\n".join(textwrap.indent(str(seg), "  ") for seg in self.segmentos)
        return f"Transcrição:\n{linhas}"
