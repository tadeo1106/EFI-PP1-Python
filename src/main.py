from fastapi import FastAPI

app = FastAPI(
    title="Cine API",
)


@app.get("/")
def root():
    return {"mensaje": "Cine API funcionando"}
