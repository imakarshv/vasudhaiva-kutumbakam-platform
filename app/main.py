@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/about.html",
        context={}
    )


@app.get("/work", response_class=HTMLResponse)
async def work(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/work.html",
        context={}
    )


@app.get("/events", response_class=HTMLResponse)
async def events(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/events.html",
        context={}
    )


@app.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/gallery.html",
        context={}
    )


@app.get("/insights", response_class=HTMLResponse)
async def insights(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/insights.html",
        context={}
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="public/contact.html",
        context={}
    )