from fastapi import FastAPI

app = FastAPI()

@app.get("/r")
def read_root():
    return {"Hello": "World"}