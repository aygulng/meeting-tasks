import time

from pydantic import ValidationError

from app.config import PROMPT_FILE, GENERATION_OPTIONS
from app.schemas.meeting import ExtractRequest, MeetingResult
from app.services import ollama
from app.services.errors import ServiceError


async def extract_tasks(request: ExtractRequest):
    available = await ollama.list_local_models()
    if request.model not in available:
        raise ServiceError(400, "Выберите установленную локальную модель из списка.")
    start = time.perf_counter()
    prompt = PROMPT_FILE.read_text(encoding="utf-8") + request.text
    for attempt in range(2):
        data = await ollama.ollama_request("POST", "/api/generate", json={
            "model": request.model, "prompt": prompt,
            "format": MeetingResult.model_json_schema(), "stream": False,
            "think": False,
            "options": GENERATION_OPTIONS,
        })
        try:
            if data.get("done_reason") == "length":
                raise ValueError("Ответ обрезан")
            result = MeetingResult.model_validate_json(data.get("response", ""))
            if any(task.evidence not in request.text for task in result.tasks):
                raise ValueError("Цитата отсутствует в заметках")
            duration = data.get("eval_duration", 0)
            return {"result": result.model_dump(), "model": request.model,
                    "seconds": round(time.perf_counter() - start, 2),
                    "tokens_per_second": round(data.get("eval_count", 0) * 1e9 / duration, 2) if duration else None,
                    "attempts": attempt + 1}
        except (ValidationError, ValueError):
            prompt += "\nВерни полный JSON по схеме. Все evidence должны быть дословными цитатами из заметок."
    raise ServiceError(422, "Модель дважды вернула неверный JSON или неподтверждённые цитаты. Попробуйте другую модель или сократите заметки.")
