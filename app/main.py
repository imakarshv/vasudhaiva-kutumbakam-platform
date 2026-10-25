from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Vasudhaiva Kutumbakam")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


# ---------------- Home ---------------- #

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/home.html",
        context={}
    )


# ---------------- About ---------------- #

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/about.html",
        context={}
    )


# ---------------- Our Work ---------------- #

@app.get("/work", response_class=HTMLResponse)
async def work(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/work.html",
        context={}
    )


# ---------------- Philosophy ---------------- #

@app.get("/philosophy", response_class=HTMLResponse)
async def philosophy(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/philosophy.html",
        context={}
    )


# ---------------- Gallery ---------------- #

@app.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/gallery.html",
        context={}
    )


# ---------------- Insights ---------------- #

@app.get("/insights", response_class=HTMLResponse)
async def insights(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/insights.html",
        context={}
    )


# ---------------- Contact ---------------- #

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/contact.html",
        context={}
    )
