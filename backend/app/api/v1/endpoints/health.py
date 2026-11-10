from functools import lru_cache

from alembic.config import Config
from alembic.script import ScriptDirectory
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_engine
from app.core.config import ROOT_DIR
from app.shared.response import failure, success

router = APIRouter(tags=['运行检查'])


@lru_cache
def migration_heads() -> set[str]:
    config = Config(str(ROOT_DIR / 'backend/alembic.ini'))
    return set(ScriptDirectory.from_config(config).get_heads())


@router.get('/health')
def health(request: Request):
    return success(request, {'status': 'ok', 'service': 'PuppleTrouble', 'version': '0.1.0', 'stage': 'bootstrap'})


@router.get('/health/ready')
def ready(request: Request):
    try:
        with get_engine().connect() as connection:
            connection.execute(text('SELECT 1'))
            revisions = set(connection.execute(text('SELECT version_num FROM alembic_version')).scalars())
            if revisions != migration_heads():
                raise ValueError('数据库迁移版本不匹配')
    except (SQLAlchemyError, ValueError):
        return JSONResponse(
            status_code=503,
            content=failure(request, 'DATABASE_NOT_READY', '数据库或迁移尚未就绪，请检查数据库并执行迁移'),
        )
    return success(request, {'status': 'ready', 'database': 'connected', 'migration': ','.join(sorted(revisions))})
