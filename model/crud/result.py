# crud.py
from sqlalchemy import func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.model.result import ResultItem


async def get_result_items(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(ResultItem)
        .where(
            ResultItem.pipeline_id == pipeline_id,
            ResultItem.score != None
        )
        .order_by(desc(ResultItem.score))
        .limit(10)
    )
    selected_rows = result.scalars().all()
    return {
        "result": selected_rows,
        # "total_count": total_count,
    }

async def get_result_items_batch(pipeline_id: int, batch: int, db: AsyncSession):
    result = await db.execute(
        select(ResultItem)
        .where(ResultItem.pipeline_id == pipeline_id, ResultItem.batch == batch, ResultItem.score != None)
        .order_by(ResultItem.iter)
    )
    return result.scalars().all()

async def get_last_iter(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(ResultItem.iter)
        .where(ResultItem.pipeline_id == pipeline_id)
        .order_by(desc(ResultItem.iter))
        .limit(1)
    )
    return result.scalar_one_or_none()