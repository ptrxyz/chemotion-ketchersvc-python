from __future__ import annotations

import multiprocessing
import sys
import uuid

from dataclasses import dataclass

from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from config import myconfig
from helper import StandaloneApplication, log
from renderer import Renderer


class GlobalAppState:
    running: bool = True
    proc: multiprocessing.Process | None = None


app = FastAPI()
globalRenderer = Renderer(myconfig)
app.add_middleware(
    CORSMiddleware,
    allow_origins=myconfig.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:

    if myconfig.debug_mode:
        print(myconfig.json(indent=4))

    if globalRenderer.initalize:
        try:
            log(f"Initalizing WebDriver. Ketcher URL: {myconfig.ketcher_url}")
            globalRenderer.init()
        except Exception as ex:  # pylint: disable=broad-except
            log(f"Failed to initalize WebDriver: {ex}")
            globalRenderer.quit()
            sys.exit(1)


@dataclass
class ReturnObject:
    task_id: str = ""
    error_code: int = 0
    msg: str = ""


@app.post("/render")
async def render(
    tid: str | None = Query(default="undefined", alias="id"),
    molfile: bytes | None = Body(),
) -> ReturnObject:
    task_id: str = tid or uuid.uuid4().hex

    if not molfile:
        return ReturnObject(task_id, 400, "No molfile provided.")

    decoded_molfile: str = molfile.decode("utf-8")
    err, ret = await globalRenderer.render(decoded_molfile)
    retobj = ReturnObject(task_id, err, ret)
    return retobj


if __name__ == "__main__":
    log("I'm starting up...")
    log(f"[{myconfig.max_workers}] workers will be started.")
    sys.stdout.flush()
    multiprocessing.freeze_support()

    options = {
        "bind": f"0.0.0.0:{myconfig.port}",
        "workers": myconfig.max_workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "accesslog": "-",
        "errorlog": "-",
        "debug": myconfig.debug_mode,
    }

    StandaloneApplication(app, options).run()
