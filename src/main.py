import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_responses import custom_openapi

from api.v1.routers import router
from auth.routes import user_router
from core import config
from core.config import app_settings

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

# app.openapi =  custom_openapi(app)
app.include_router(router, prefix='/api/v1')
app.include_router(user_router, prefix='/api/v1/auth')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        reload=True
    )
