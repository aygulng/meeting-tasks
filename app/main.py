from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import meetings, models
from app.config import WEB_DIR
from app.services.errors import ServiceError


def create_app() -> FastAPI:
    application = FastAPI(title="Задачи из встречи — локальная LLM")
    application.include_router(models.router, prefix="/api", tags=["models"])
    application.include_router(meetings.router, prefix="/api", tags=["meetings"])
    application.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

    @application.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @application.get("/", include_in_schema=False)
    def index():
        return FileResponse(WEB_DIR / "index.html")

    return application


app = create_app()
