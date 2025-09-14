from fastapi import FastAPI
from controller.ChatController import chatrouter
from middleware.LoggingMiddleware import LoggingMiddleware



app = FastAPI()
app.include_router(chatrouter)
app.add_middleware(LoggingMiddleware)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
