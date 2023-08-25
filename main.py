from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()

@app.get('/test')
async def test(message: str = Query(None, alias="message")):
    content = f"""<html>
                    <head>
                        <title>Test Page</title>
                    </head>
                    <body>
                        <h1>Test Page</h1>
                        <p>Message: {message}</p>
                    </body>
                  </html>"""
    return HTMLResponse(content=content, status_code=200)

@app.get('/')
async def test():
    content = f"""<html>
                    <head>
                        <title>Test Page</title>
                    </head>
                    <body>
                        <h1>Test Page</h1>
                        <p>Message: Hello, This is a very simple page created by FastAPI </p>
                    </body>
                  </html>"""
    return HTMLResponse(content=content, status_code=200)
