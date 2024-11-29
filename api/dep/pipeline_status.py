from sqlalchemy.ext.asyncio import AsyncSession
from model.crud import pipeline_status as crud_stauts


async def init_status(pipeline_id: int, db: AsyncSession):
    return await crud_stauts.create_item(pipeline_id, db)


async def update_status_step(pipeline_id: int, step: str, db: AsyncSession):
    return await crud_stauts.update_step(pipeline_id, step, db)


async def update_status_iter(pipeline_id: int, iter: int, db: AsyncSession):
    return await crud_stauts.update_iter(pipeline_id, iter, db)


async def check_status_iter(pipeline_id: int, db: AsyncSession):
    return await crud_stauts.check_iter(pipeline_id, db)


async def check_status_step(pipeline_id: int, db: AsyncSession):
    return await crud_stauts.check_step(pipeline_id, db)