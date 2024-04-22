from typing import Optional
from pydantic import AliasGenerator, BaseModel, ConfigDict, HttpUrl
from pydantic.alias_generators import to_snake, to_camel

from datetime import datetime


class GitHubRepositoryResponse(BaseModel):
    full_name: str
    description: Optional[str] = None
    clone_url: HttpUrl
    stargazers_count: int
    created_at: datetime


class RepositorySchema(BaseModel):
    full_name: str
    description: Optional[str] = None
    clone_url: HttpUrl
    stars: int
    created_at: datetime

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        )
    )
