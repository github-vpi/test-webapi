from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from qdrant_client import QdrantClient
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Header, APIRouter, HTTPException, FastAPI, UploadFile, File, Request, Form, Query
import pandas as pd
import json as json
@app.post('/getfile')
async def upload_csv(csv_file: UploadFile = File(...)):
    # Check if the uploaded file is a CSV file
    if csv_file.content_type != "text/csv":
        raise HTTPException(status_code=415, detail="File attached is not a CSV file")
    
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file.file)
        return {"result": df}
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file 1")

@app.get('/qdrant')
async def qdrant():

    CD_QDRANT_URL = 'https://2aaeafec-b03e-4545-9b12-f8f806ad320a.eu-central-1-0.aws.cloud.qdrant.io:6333'
    CD_QDRANT_API_KEY = 'QoB7detTXir9bCdMhGNP9tPdWs61VUWChrH9tROY6YXgo4wtD6LNCg'
    collection_name = 'context'
    
    qdrant_client = QdrantClient(url=CD_QDRANT_URL, api_key=CD_QDRANT_API_KEY)
    
    all_points = qdrant_client.scroll(
                    collection_name=collection_name, 
                    limit=1000,
                    with_payload=True,
                    with_vectors=False,
                )
    full_txt = ''
    for i in range(len(all_points[0])):
        full_txt += all_points[0][i].payload['page_content'] + '\n'
    
    response = {}
    response['context'] = full_txt
    return response


@app.get('/qdrantkey')
async def qdrantkey(qdrant_api_key: str = Query(None, alias="qdrant_api_key")):

    CD_QDRANT_URL = 'https://2aaeafec-b03e-4545-9b12-f8f806ad320a.eu-central-1-0.aws.cloud.qdrant.io:6333'
    CD_QDRANT_API_KEY = qdrant_api_key
    # CD_QDRANT_API_KEY = 'QoB7detTXir9bCdMhGNP9tPdWs61VUWChrH9tROY6YXgo4wtD6LNCg'
    collection_name = 'context'
    
    qdrant_client = QdrantClient(url=CD_QDRANT_URL, api_key=CD_QDRANT_API_KEY)
    
    all_points = qdrant_client.scroll(
                    collection_name=collection_name, 
                    limit=1000,
                    with_payload=True,
                    with_vectors=False,
                )
    full_txt = ''
    for i in range(len(all_points[0])):
        full_txt += all_points[0][i].payload['page_content'] + '\n'
    
    response = {}
    response['context'] = full_txt
    return response


@app.get('/testabc')
async def testabc(message: str = Query(None, alias="message")):
    response = {}
    response['context'] = message
    return response


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
async def index():
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
