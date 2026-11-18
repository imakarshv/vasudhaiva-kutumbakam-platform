from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

from fastapi import Form
from fastapi.responses import RedirectResponse



app = FastAPI(title="Vasudhaiva Kutumbakam")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")
# ---------------- Idea Submissions Database ---------------- #

def create_ideas_table():
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS idea_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            private_discussion INTEGER,
            idea_title TEXT NOT NULL,
            problem TEXT NOT NULL,
            solution TEXT NOT NULL,
            beneficiaries TEXT NOT NULL,
            evidence TEXT,
            implementation TEXT,
            support TEXT,
            participation TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


create_ideas_table()

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

# ---------------- From Thought to Action ---------------- #

@app.get("/work", response_class=HTMLResponse)
async def work(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/our-ideas.html",
        context={}
    )



# ---------------- Submit an Idea ---------------- #

@app.post("/submit-idea")
async def submit_idea(
    name: str = Form(...),
    contact: str = Form(...),
    private_discussion: str | None = Form(None),
    idea_title: str = Form(...),
    problem: str = Form(...),
    solution: str = Form(...),
    beneficiaries: str = Form(...),
    evidence: str = Form(""),
    implementation: str = Form(""),
    support: str = Form(""),
    participation: str = Form(...)
):
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        INSERT INTO idea_submissions (
            name, contact, private_discussion,
            idea_title, problem, solution,
            beneficiaries, evidence, implementation,
            support, participation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        contact,
        1 if private_discussion else 0,
        idea_title,
        problem,
        solution,
        beneficiaries,
        evidence,
        implementation,
        support,
        participation
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/work?submitted=true",
        status_code=303
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
