from fastapi import FastAPI

app = FastAPI(title="Project Invoice API")


@app.get("/")
def home():
    return {"message": "서버가 동작 중입니다"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
