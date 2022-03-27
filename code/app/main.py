import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from utilities.utilities_metadata import metadata_pdf, create_json_pdf, all_keys
from utilities.utilities_references import create_json_referenes, references_pdf


app = FastAPI()


@app.get("/")
async def root():
    return [{"message": "This API is to store data from pdf files (extracted from the site arxiv) in a JSON file"}, 
    {"/extract_metadata/{pdf_id}" : "to extract metadata and store in JSON file"},
    {"/extract_references/{pdf_id}" : "to extract references and store in JSON file"},
    {"/metadata/{pdf_id}" : "to display extracted metadata"},
    {"/references/{pdf_id}" : "to display extracted references"},
    {"/all/" : "show all extracted pdf_id"}]

@app.get("/extract_metadata/{pdf_id}")
def update_metadata(pdf_id):
    create_json_pdf(pdf_id)
    return metadata_pdf(pdf_id)

@app.get("/extract_references/{pdf_id}")
def update_references(pdf_id):
    create_json_referenes(pdf_id)
    return references_pdf(pdf_id)

@app.get("/metadata/{pdf_id}")
async def read_metadata(pdf_id):
    return metadata_pdf(pdf_id)

@app.get("/references/{pdf_id}")
async def read_references(pdf_id):
    return references_pdf(pdf_id)

@app.get("/all/")
async def read_all():
    return all_keys()

# OpenApi
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Metadata and References extraction from pdf_id in ArXiv",
        version="1.1.0",
        description="This OpenApi Scheme describes how to use this application",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)