from fastapi import FastAPI, UploadFile, File
import uvicorn

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile):
    content = file.file.read()
    with open(file.filename, "wb") as f:
        f.write(content)
    return {"filename": file.filename}

if __name__ == '__main__':
    uvicorn.run(app)