from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from functions.read_settings import ReadSettingsFile
from functions.syncronize import scheduler
from functions.url_handle import UrlHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("@SERVIDOR INICIANDO@")
    await ReadSettingsFile.read()
    yield
    scheduler.shutdown()
    print("#SERVIDOR TERMINANDO#")


app = FastAPI(lifespan=lifespan)


@app.route("/healthcheck", methods=["GET"])
async def hello(request: Request):
    return JSONResponse("Healthy")


@app.api_route("/{path_name:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def catch_all(request: Request, path_name: str):

    from_function = await UrlHandler.find_matching_url(path_name)

    return {
        "request_method": request.method,
        "path_name": path_name,
        "query_params": request.query_params,
        "headers": request.headers,
        "body": await request.body(),
        "from_function": from_function,
    }
