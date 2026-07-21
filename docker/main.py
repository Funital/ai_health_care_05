from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello_handler():
    return {"message": "Hello"}

@app.get("/hi")
def hi_handler():
    return {"message": "Hi"}