from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.github import GithubRepository, GithubCommit, GithubPullRequest, GithubIssue
from app.infrastructure.persistence.postgres.models.github_models import (
    RepositoryModel,
    CommitModel,
    PullRequestModel,
    IssueModel
)


class PostgresGithubRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_repository(self, entity: GithubRepository) -> RepositoryModel:
        stmt = select(RepositoryModel).where(RepositoryModel.github_repo_id == entity.github_repo_id)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()

        if model:
            model.name = entity.name
            model.full_name = entity.full_name
            model.url = entity.url
            model.default_branch = entity.default_branch
            model.is_private = entity.is_private
            model.language = entity.language
            model.updated_at = entity.updated_at
        else:
            model = RepositoryModel(
                id=entity.id,
                org_id=entity.org_id,
                github_repo_id=entity.github_repo_id,
                name=entity.name,
                full_name=entity.full_name,
                url=entity.url,
                default_branch=entity.default_branch,
                is_private=entity.is_private,
                language=entity.language,
                created_at=entity.created_at,
                updated_at=entity.updated_at
            )
            self.session.add(model)

        await self.session.flush()
        return model

    async def upsert_commit(self, entity: GithubCommit) -> CommitModel:
        stmt = select(CommitModel).where(CommitModel.sha == entity.sha)
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()

        if not model:
            model = CommitModel(
                id=entity.id,
                repo_id=entity.repo_id,
                sha=entity.sha,
                author_email=entity.author_email,
                author_name=entity.author_name,
                message=entity.message,
                additions=entity.additions,
                deletions=entity.deletions,
                committed_at=entity.committed_at
            )
            self.session.add(model)
            await self.session.flush()

        return model

    async def upsert_pull_request(self, entity: GithubPullRequest) -> PullRequestModel:
        stmt = select(PullRequestModel).where(
            PullRequestModel.repo_id == entity.repo_id,
            PullRequestModel.github_pr_number == entity.github_pr_number
        )
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()

        if model:
            model.title = entity.title
            model.state = entity.state
            model.additions = entity.additions
            model.deletions = entity.deletions
            model.changed_files = entity.changed_files
            model.merged_at = entity.merged_at
            model.closed_at = entity.closed_at
        else:
            model = PullRequestModel(
                id=entity.id,
                repo_id=entity.repo_id,
                github_pr_number=entity.github_pr_number,
                title=entity.title,
                state=entity.state,
                author_username=entity.author_username,
                source_branch=entity.source_branch,
                target_branch=entity.target_branch,
                additions=entity.additions,
                deletions=entity.deletions,
                changed_files=entity.changed_files,
                created_at=entity.created_at,
                merged_at=entity.merged_at,
                closed_at=entity.closed_at
            )
            self.session.add(model)

        await self.session.flush()
        return model

    async def upsert_issue(self, entity: GithubIssue) -> IssueModel:
        stmt = select(IssueModel).where(
            IssueModel.repo_id == entity.repo_id,
            IssueModel.github_issue_number == entity.github_issue_number
        )
        res = await self.session.execute(stmt)
        model = res.scalar_one_or_none()

        if model:
            model.title = entity.title
            model.state = entity.state
            model.closed_at = entity.closed_at
        else:
            model = IssueModel(
                id=entity.id,
                repo_id=entity.repo_id,
                github_issue_number=entity.github_issue_number,
                title=entity.title,
                state=entity.state,
                author_username=entity.author_username,
                created_at=entity.created_at,
                closed_at=entity.closed_at
            )
            self.session.add(model)

        await self.session.flush()
        return model

    async def get_by_full_name(self, full_name: str) -> Optional[RepositoryModel]:
        stmt = select(RepositoryModel).where(RepositoryModel.full_name == full_name)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_by_org(self, org_id: uuid.UUID) -> List[RepositoryModel]:
        stmt = select(RepositoryModel).where(RepositoryModel.org_id == org_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
