from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from qdrant_client import QdrantClient
import json

app = FastAPI()

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
    #json_string = json.dumps(response)
    #print(response)
    return response
    #return {"message": "Hello World", "Note": "This is a test 12"}


@app.get('/qdrantkey')
async def qdrantkey(qdrant-api-key: str = Query(None, alias="qdrant-api-key")):

    CD_QDRANT_URL = 'https://2aaeafec-b03e-4545-9b12-f8f806ad320a.eu-central-1-0.aws.cloud.qdrant.io:6333'
    CD_QDRANT_API_KEY = qdrant-api-key
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
    #json_string = json.dumps(response)
    #print(response)
    return response
    #return {"message": "Hello World", "Note": "This is a test1"}

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
