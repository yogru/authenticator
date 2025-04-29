from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from src.present.rest.v1.sync_router import rt as sync_router
from src.present.rest.v1.token_router import rt as token_router
app = FastAPI(
    title="authenticator",
    description="authenticator",
    version="0.1.0",
    docs_url='/apidocs',
    redoc_url='/apiredoc',
    openapi_url='/openapi.json',
)

origins = [
    "https://negot.ktcommerce.co.kr",
]

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://localhost:3000", "http://localhost:21200", "http://localhost:22000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Authenticator API"}


app.include_router(sync_router, prefix='/api/v1')
app.include_router(token_router, prefix='/api/v1')