from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from .utils import logger
from .schemas import RepositorySchema
from .dao.crud import RepositoryCRUD, create_tables, get_db
from .external.github_api import fetch_repository_details
import httpx

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        await create_tables()
        logger.info("App started successfully.")
    except Exception as e:
        logger.error(f"Error occurred while App starting: {str(e)}")
        raise e


@app.get("/status", response_model=dict)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Try to execute a simple non-blocking database operation
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except SQLAlchemyError as e:
        # If there's a database connection issue, return an unhealthy status
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "details": str(e)})


@app.get("/repositories/{owner}/{repo}", response_model=RepositorySchema)
async def read_repository(owner: str, repo: str, db: AsyncSession = Depends(get_db)):
    repo_full_name = f"{owner}/{repo}"

    # Attempt to retrieve from the database first
    try:
        db_repo = await RepositoryCRUD.get_repository(db, repo_full_name)
        if db_repo:
            logger.info(f"Successfully retrieved repository {repo_full_name} from the database")
            return db_repo
    except SQLAlchemyError as e:
        logger.warning(f"Error occurred when retrieving repository from the database: {e}")

    # Fetch from GitHub if not found in the database
    try:
        gh_repo = await fetch_repository_details(owner, repo)
    except httpx.HTTPStatusError as e:
        logger.error(f"GitHub repository not found: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="GitHub repository not found")

    repo_data = {
        "full_name": gh_repo.full_name,
        "description": gh_repo.description,
        "clone_url": str(gh_repo.clone_url),
        "stars": gh_repo.stargazers_count,
        "created_at": gh_repo.created_at.replace(tzinfo=None),
        "last_accessed": datetime.utcnow(),
    }

    # Add new repository to the database
    try:
        await RepositoryCRUD.add_repository(db, repo_data)
        logger.info(f"Successfully added repository {repo_full_name} to the database")
    except SQLAlchemyError as e:
        logger.warning(f"Error occurred when adding repository to the database: {e}")

    return repo_data
