from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.models import Repository
from app.utils import logger


class RepositoryCRUD:

    @classmethod
    async def get_repository(cls, db_session: AsyncSession, full_name: str):
        """Get a repository by its full name with caching logic."""
        current_time = datetime.utcnow()
        result = await db_session.execute(
            select(Repository).where(Repository.full_name == full_name)
        )
        repo = result.scalars().first()
        logger.info(f"Get repository result {repo} from full_name {full_name}")
        if repo:
            if (current_time - repo.last_accessed).total_seconds() < repo.ttl:
                return repo
            else:
                cls.delete_repository(db_session, full_name)
        return None

    @classmethod
    async def add_repository(cls, db_session: AsyncSession, repo_data):
        """Add a new repository to the database."""
        try:
            logger.warning(f"Add repository with repository data dict {repo_data}")

            full_name = repo_data["full_name"]
            result = await db_session.execute(
                select(Repository).where(Repository.full_name == full_name)
            )
            repository_exist = result.scalars().first()
            if repository_exist:
                logger.warning(f"Repository {full_name} already exists in the database")
                await cls.update_repository(db_session, full_name, repo_data)
            else:
                new_repo = Repository(**repo_data)
                db_session.add(new_repo)
                await db_session.commit()
                await db_session.refresh(new_repo)

                logger.info(f"Successfully added repository {repo_data} to the database")
        except Exception as e:
            logger.error(f"Error occurred when adding repository to the database: {e}")
            raise e

    @classmethod
    async def update_repository(cls, db_session: AsyncSession, full_name, update_data):
        """Update a repository by its full name in the database."""
        try:
            # Fetch the repository to update
            result = await db_session.execute(
                select(Repository).where(Repository.full_name == full_name)
            )
            repository_to_update = result.scalars().first()

            if repository_to_update:
                # Update the repository fields with new data
                for key, value in update_data.items():
                    if hasattr(repository_to_update, key):
                        setattr(repository_to_update, key, value)

                # Commit the changes to the database
                await db_session.commit()
                await db_session.refresh(repository_to_update)
                logger.info(f"Successfully updated repository with full name: {full_name}")
            else:
                # Log if no repository is found with the provided full name
                logger.warning(f"No repository found with full name: {full_name} to update.")

        except Exception as e:
            logger.error(f"Error occurred when updating the repository: {e}")
            raise e

    @classmethod
    async def delete_repository(cls, db_session: AsyncSession, full_name):
        """Delete a repository by its full name from the database."""
        try:
            # Fetch the repository to delete
            result = await db_session.execute(
                select(Repository).where(Repository.full_name == full_name)
            )
            repository_to_delete = result.scalars().first()

            if repository_to_delete:
                # Delete the repository if it exists
                db_session.delete(repository_to_delete)
                await db_session.commit()
                logger.info(f"Successfully deleted repository with full name: {full_name}")
            else:
                # Log if no repository is found with the provided full name
                logger.warning(f"No repository found with full name: {full_name} to delete.")

        except Exception as e:
            logger.error(f"Error occurred when deleting the repository: {e}")
            raise e
