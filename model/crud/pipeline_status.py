# crud.py
from sqlalchemy import func, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.model.pipeline_status import PipelineStatusItem


async def get_pipeline_status_items(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineStatusItem).where(PipelineStatusItem.pipeline_id == pipeline_id)
    )
    selected_rows = result.scalar_one_or_none()
    return {
        "result": selected_rows,
        # "total_count": total_count,
    }


async def create_item(pipeline_id: int, db: AsyncSession):
    new_item = PipelineStatusItem(
        pipeline_id=pipeline_id, iter=1, step=0
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


async def update_step(pipeline_id: int, step: int, db: AsyncSession):
    await db.execute(
        update(PipelineStatusItem)
        .where(PipelineStatusItem.pipeline_id == pipeline_id)
        .values(step=step)
    )
    await db.commit()
    return


async def check_iter(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineStatusItem.iter).where(
            PipelineStatusItem.pipeline_id == pipeline_id
        )
    )
    return result.scalar_one_or_none()


async def check_step(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineStatusItem.step).where(
            PipelineStatusItem.pipeline_id == pipeline_id
        )
    )
    return result.scalar_one_or_none()


async def update_iter(pipeline_id: int, iter: int, db: AsyncSession):
    await db.execute(
        update(PipelineStatusItem)
        .where(PipelineStatusItem.pipeline_id == pipeline_id)
        .values(iter=iter)
    )
    await db.commit()
    return