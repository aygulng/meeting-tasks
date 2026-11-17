import httpx

from app.config import OLLAMA_URL, OLLAMA_TIMEOUT
from app.services.errors import ServiceError


async def ollama_request(method, path, **kwargs):
    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT, trust_env=False) as client:
            response = await client.request(method, OLLAMA_URL + path, **kwargs)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise ServiceError(504, "Модель не ответила за 240 секунд. Попробуйте меньшую модель или более короткий текст.")
    except httpx.HTTPStatusError as exc:
        raise ServiceError(502, f"Ollama вернула ошибку {exc.response.status_code}. Проверьте модель и журнал Ollama.")
    except (httpx.RequestError, ValueError):
        raise ServiceError(503, "Ollama недоступна или вернула неверный ответ. Запустите Ollama и обновите список моделей.")


async def list_local_models() -> list[str]:
    data = await ollama_request("GET", "/api/tags")
    # Cloud models are intentionally excluded from this local-only application.
    return [m["name"] for m in data.get("models", [])
                       if not m.get("remote_host") and "cloud" not in m["name"].lower()]


