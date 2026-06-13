import pytest
import respx
import httpx
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sysnet_cites_core_types.database import Base
from sysnet_cites_core_engine.repository import PostgreSQLRepository
from sysnet_cites_legacy_adapter.client import LegacyDocsClient
from sysnet_cites_legacy_adapter.migration import LegacyMigrationEngine

TEST_DB_URL = "postgresql+asyncpg://docker:docker@localhost:25432/docker"

@pytest_asyncio_fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture
async def session(engine):
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        yield session

@pytest.mark.asyncio
@respx.mock
async def test_full_migration_workflow(session):
    # 1. Mock Legacy API
    legacy_url = "http://legacy.internal"
    mock_legacy_data = [
        {
            "document_id": "MIGRATE-001",
            "state": "SCHVÁLENO",
            "issued_at": "2026-01-01T00:00:00",
            "exporter": {"name": "Old Exp", "country": "CZ"},
            "importer": {"name": "Old Imp", "country": "SK"},
            "items": [{"taxon_id": "T1", "appendix": "I", "quantity": 10.0, "source": "W", "purpose": "T"}]
        }
    ]
    
    respx.get(f"{legacy_url}/api/v1/documents").mock(return_value=httpx.Response(200, json=mock_legacy_data))

    # 2. Setup Components
    repo = PostgreSQLRepository(session)
    client = LegacyDocsClient(base_url=legacy_url)
    engine = LegacyMigrationEngine(legacy_client=client, repository=repo)

    # 3. Execute Migration
    result = await engine.migrate_all()
    await session.commit()

    # 4. Verify Results
    assert result["total"] == 1
    assert result["migrated"] == 1
    assert len(result["errors"]) == 0

    # 5. Verify in DB
    migrated_permit = await repo.get_permit("MIGRATE-001")
    assert migrated_permit is not None
    assert migrated_permit.exporter.name == "Old Exp"
    assert migrated_permit.items[0].taxon_id == "T1"
