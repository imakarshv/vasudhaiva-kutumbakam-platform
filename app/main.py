from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

from fastapi import Form
from fastapi.responses import RedirectResponse

from fastapi import HTTPException

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


def create_contributors_table():
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS contributor_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            location TEXT NOT NULL,
            interests TEXT NOT NULL,
            skills TEXT NOT NULL,
            experience TEXT,
            availability TEXT NOT NULL,
            contributions TEXT NOT NULL,
            message TEXT,
            additional_info TEXT,
            consent INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


create_contributors_table()


def create_seva_volunteers_table():
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS seva_volunteer_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            activities TEXT NOT NULL,
            skills TEXT NOT NULL,
            contributions TEXT NOT NULL,
            availability TEXT NOT NULL,
            mode TEXT NOT NULL,
            accessibility TEXT,
            consent INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


create_seva_volunteers_table()

def create_sikshana_table():
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sikshana_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            location TEXT NOT NULL,
            role TEXT NOT NULL,
            expertise TEXT,
            qualifications TEXT,
            topics TEXT,
            preferred_format TEXT NOT NULL,
            availability TEXT NOT NULL,
            additional_info TEXT,
            consent INTEGER NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


create_sikshana_table()

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

@app.post("/submit-contributor")
async def submit_contributor(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    location: str = Form(...),
    interests: list[str] = Form(...),
    skills: list[str] = Form(...),
    experience: str = Form(""),
    availability: str = Form(...),
    contributions: list[str] = Form(...),
    message: str = Form(""),
    additional_info: str = Form(""),
    consent: str = Form(...)
):
    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        INSERT INTO contributor_submissions (
            name, email, phone, location,
            interests, skills, experience,
            availability, contributions,
            message, additional_info, consent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        location,
        ", ".join(interests),
        ", ".join(skills),
        experience,
        availability,
        ", ".join(contributions),
        message,
        additional_info,
        1 if consent == "yes" else 0
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/work?contributor_submitted=true",
        status_code=303
    )

@app.post("/submit-seva-volunteer")
async def submit_seva_volunteer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    location: str = Form(...),
    activities: list[str] = Form(...),
    skills: str = Form(...),
    contributions: list[str] = Form(...),
    availability: str = Form(...),
    mode: str = Form(...),
    accessibility: str = Form(""),
    consent: str = Form(...)
):
    allowed_activities = {
        "Environment and Nature",
        "Water Resources and Climate Action",
        "Education and Mentoring",
        "Elderly Care",
        "Healthcare and Donation",
        "Food and Essential Needs",
        "Livelihoods and Economic Empowerment",
        "Women Empowerment and Inclusion",
        "Civic Responsibility",
        "Community Infrastructure",
        "Disaster Relief",
        "Knowledge and Technology",
        "Yoga, Meditation and Sports",
        "Giving and Community Solidarity"
    }

    allowed_contributions = {
        "Time",
        "Expertise",
        "Physical effort",
        "Resources",
        "Financial support"
    }

    if not activities or not set(activities).issubset(allowed_activities):
        raise HTTPException(
            status_code=400,
            detail="Please select at least one valid SEVA activity."
        )

    if not contributions or not set(contributions).issubset(allowed_contributions):
        raise HTTPException(
            status_code=400,
            detail="Please select at least one valid contribution."
        )

    if consent != "yes":
        raise HTTPException(
            status_code=400,
            detail="Consent is required."
        )

    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        INSERT INTO seva_volunteer_submissions (
            name, email, phone, location, activities,
            skills, contributions, availability, mode,
            accessibility, consent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        location,
        ", ".join(activities),
        skills,
        ", ".join(contributions),
        availability,
        mode,
        accessibility,
        1
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/work?seva_submitted=true",
        status_code=303
    )

@app.post("/submit-sikshana")
async def submit_sikshana(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    location: str = Form(...),
    role: str = Form(...),
    expertise: str = Form(""),
    qualifications: str = Form(""),
    topics: str = Form(""),
    format: str = Form(...),
    availability: str = Form(...),
    additional_info: str = Form(""),
    consent: str = Form(...)
):
    allowed_roles = {
        "Teacher / Mentor",
        "Learner",
        "Both"
    }

    allowed_formats = {
        "Online",
        "In-person",
        "Either"
    }

    allowed_availability = {
        "One-time",
        "Occasional",
        "Regular",
        "Flexible"
    }

    if role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Please select a valid participation role."
        )

    if format not in allowed_formats:
        raise HTTPException(
            status_code=400,
            detail="Please select a valid preferred format."
        )

    if availability not in allowed_availability:
        raise HTTPException(
            status_code=400,
            detail="Please select a valid availability."
        )

    if consent != "yes":
        raise HTTPException(
            status_code=400,
            detail="Consent is required."
        )

    connection = sqlite3.connect("ideas.db")

    connection.execute("""
        INSERT INTO sikshana_submissions (
            name, email, phone, location, role,
            expertise, qualifications, topics,
            preferred_format, availability,
            additional_info, consent
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        location,
        role,
        expertise,
        qualifications,
        topics,
        format,
        availability,
        additional_info,
        1
    ))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/work?sikshana_submitted=true",
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
