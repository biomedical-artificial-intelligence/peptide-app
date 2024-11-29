from fastapi import FastAPI
from api.v1 import router as v1_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(v1_router, prefix="")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8004)