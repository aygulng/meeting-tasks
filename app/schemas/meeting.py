from pydantic import BaseModel, ConfigDict, Field, field_validator


class Task(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task: str = Field(min_length=1)
    owner: str | None
    deadline: str | None
    evidence: str = Field(min_length=1, description="Дословная цитата из заметок")


class MeetingResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tasks: list[Task]


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    model: str = Field(min_length=1, max_length=100)

    @field_validator("text", "model")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Поле не должно быть пустым")
        return value.strip()


class ExtractResponse(BaseModel):
    result: MeetingResult
    model: str
    seconds: float
    tokens_per_second: float | None
    attempts: int


class ModelsResponse(BaseModel):
    models: list[str]
