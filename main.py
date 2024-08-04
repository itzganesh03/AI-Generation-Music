from fastapi import FastAPI

if __name__ == "__main__":
    app = FastAPI()


    @app.get("/r")
    def read_root():
        return {"Hello": "World"}