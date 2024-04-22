import httpx
from ..config import settings
from ..utils import logger
from ..schemas import GitHubRepositoryResponse

global_timeout = httpx.Timeout(timeout=settings.github_api_timeout)  # in seconds


async def fetch_repository_details(owner: str, repo: str) -> GitHubRepositoryResponse:
    try:
        url = f"{settings.github_api_base_url}/{owner}/{repo}"
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=settings.github_api_timeout)) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raises exception for HTTP error responses
            data = response.json()
            logger.info(f"Successfully fetched repository details for {owner}/{repo}")
            return GitHubRepositoryResponse.parse_obj(data)
    except Exception as e:
        logger.error(f"Error occurred while fetching repository details for {owner}/{repo}: {str(e)}")
        raise e
