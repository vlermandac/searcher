from pydantic import BaseModel
from typing import List, Annotated
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from main import Main

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "*"
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def submit(request: Request, input_text: Annotated[str, Form()]):
    main = Main()
    # items = {"kg": main.run("--KG", query=input_text),
    #          "rag": main.run("--RAG", query=input_text)}
    items = {"rag": main.run("--RAG", query=input_text)}
    return templates.TemplateResponse("response.html", {"request":
                                                        request, **items})
