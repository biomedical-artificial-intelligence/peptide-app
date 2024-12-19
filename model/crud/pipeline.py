# crud.py
from sqlalchemy import func, update, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from model.model.pipeline import PipelineItem


async def get_item(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineItem).where(PipelineItem.id == pipeline_id)
    )
    return result.scalar_one_or_none()


# def get_all_items(db: AsyncSession, skip: int = 0, limit: int = 10):
async def get_all_items(db: AsyncSession):
    result = await db.execute(
        select(PipelineItem)
        .where(PipelineItem.status != None)
        .order_by(desc(PipelineItem.id))
    )
    data = result.scalars().all()
    total_count = len(data)
    return {
        "result": data,
        "total_count": total_count,
    }


async def create_item(db: AsyncSession, item: PipelineItem):
    db_item = item
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    # result_row = db.query(PipelineItem).filter(PipelineItem.id == db_item.id).first()
    # last_id = db.query(func.max(PipelineItem.id)).scalar()
    # db_item["id"] = last_id
    return db_item.id


async def check_status(db: AsyncSession, id: int):
    result = db.query(PipelineItem.id, PipelineItem.progress).get(id)
    if result:
        return f"result: {result}"
    else:
        return "Pipeline ID not found"


async def update_status(db: AsyncSession, id: int, progress: int):
    pipeline = db.query(PipelineItem.id, PipelineItem.progress).get(id)
    pipeline.progress = progress
    db.commit()
    db.refresh(pipeline)
    return pipeline


async def check_directory_name(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineItem.dir_name).where(PipelineItem.id == pipeline_id)
    )
    return result.scalar_one_or_none()


async def create_new_directory(pipeline_id: int, db: AsyncSession):
<<<<<<< HEAD
    result = await db.execute(
        select(PipelineItem.receptor).where(PipelineItem.id == pipeline_id)
    )
    pdb = result.scalar_one_or_none()
    result = await db.execute(select(PipelineItem.dir_name))
    ALL_DIR = result.scalars().all()
    unq = 1
    NEW_DIR = "{}-{}".format(Path(pdb).stem, str(unq).zfill(3))

    while NEW_DIR in ALL_DIR:
        unq += 1
        NEW_DIR = "{}-{}".format(Path(pdb).stem, str(unq).zfill(3))
        result = await db.execute(select(PipelineItem.dir_name))
        ALL_DIR = result.scalars().all()

    result = await db.execute(
        update(PipelineItem)
        .where(PipelineItem.id == pipeline_id)
        .values(dir_name=NEW_DIR)
    )
=======
    result_class = await db.execute(
        select(PipelineItem.class_id).where(PipelineItem.id == pipeline_id)
    )
    class_id = result_class.scalar_one_or_none()
    if class_id == 1:
        result = await db.execute(
            select(PipelineItem.receptor).where(PipelineItem.id == pipeline_id)
        )
        pdb = result.scalar_one_or_none()
        result = await db.execute(select(PipelineItem.dir_name))
        ALL_DIR = result.scalars().all()
        unq = 1
        NEW_DIR = "{}-{}".format(Path(pdb).stem, str(unq).zfill(3))

        while NEW_DIR in ALL_DIR:
            unq += 1
            NEW_DIR = "{}-{}".format(Path(pdb).stem, str(unq).zfill(3))
            result = await db.execute(select(PipelineItem.dir_name))
            ALL_DIR = result.scalars().all()

        result = await db.execute(
            update(PipelineItem)
            .where(PipelineItem.id == pipeline_id)
            .values(dir_name=NEW_DIR)
        )
    elif class_id == 2:
        result = await db.execute(
            select(PipelineItem.name).where(PipelineItem.id == pipeline_id)
        )
        name = result.scalar_one_or_none()
        unq = 1
        NEW_DIR = "{}-{}".format(Path(name).stem, str(unq).zfill(3))
        result = await db.execute(select(PipelineItem.dir_name))
        ALL_DIR = result.scalars().all()

        while NEW_DIR in ALL_DIR:
            unq += 1
            NEW_DIR = "{}-{}".format(Path(name).stem, str(unq).zfill(3))
            result = await db.execute(select(PipelineItem.dir_name))
            ALL_DIR = result.scalars().all()

        result = await db.execute(
            update(PipelineItem)
            .where(PipelineItem.id == pipeline_id)
            .values(dir_name=NEW_DIR)
        )
>>>>>>> e2c2703 (update)
    await db.commit()
    return NEW_DIR


async def get_max_iter(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
        select(PipelineItem.max_iter).where(PipelineItem.id == pipeline_id)
    )
    return result.scalar_one_or_none()


async def finish_item(pipeline_id: int, db: AsyncSession):
    result = await db.execute(
<<<<<<< HEAD
        update(PipelineItem)
        .where(PipelineItem.id == pipeline_id)
        .values(status="DONE")
=======
        update(PipelineItem).where(PipelineItem.id == pipeline_id).values(status="DONE")
>>>>>>> e2c2703 (update)
    )
    await db.commit()
    return


# def update_item(db: AsyncSession, item_id: int, item: ItemUpdate):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item:
#         for key, value in item.dict().items():
#             setattr(db_item, key, value)
#         db.commit()
#         db.refresh(db_item)
#     return db_item

# def delete_item(db: AsyncSession, item_id: int):
#     db_item = db.query(Item).filter(Item.id == item_id).first()
#     if db_item:
#         db.delete(db_item)
#         db.commit()
#     return db_item