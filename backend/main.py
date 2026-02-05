from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from api.company_routers import router as company_routers
from api.branch_routers import router as branch_routers

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="IMS API's",
    description="APIs for Inventory Management System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(company_routers, prefix="/api/v1")
app.include_router(branch_routers, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {
        "Message" : "Welcome to the IMS API's",
        "Author" : "Emmanuel R",
        "Version" : "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("SERVER_PORT")))