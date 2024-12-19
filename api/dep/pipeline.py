# from fastapi import Depends
import asyncio, pytz, os
from pathlib import Path
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from model.model.pipeline import PipelineItem
from model.crud import pipeline as crud_pipeline
from model.crud import result as crud_result
from api.dep import pipeline_status as dep_status
from api.dep.pipeline_model_client import (
    BanditModelClient,
    FoldModelClient,
    DockModelClient,
)

burl = os.getenv("BANDIT_SERVER")
furl = os.getenv("FOLD_SERVER")
durl = os.getenv("DOCK_SERVER")


async def get_pipeline_items(db: AsyncSession):
    pipeline_list = await crud_pipeline.get_all_items(db)
    return {
        "data": {
            "result_list": [
                {
                    "id": pipeline.id,
                    # "ligand": Path(pipeline.ligand).stem,
                    "receptor": Path(pipeline.receptor).stem,
                    "created_at": pipeline.created_at.replace(tzinfo=pytz.UTC)
                    .astimezone(pytz.timezone("Asia/Seoul"))
                    .strftime("%Y-%m-%d %H:%M:%S"),
<<<<<<< HEAD
                    "status": pipeline.status
=======
                    "status": pipeline.status,
>>>>>>> e2c2703 (update)
                }
                for pipeline in pipeline_list["result"]
            ],
            "total_count": pipeline_list["total_count"],
        }
    }


async def init_new_pipeline(
<<<<<<< HEAD
    # sequence: str = Form(...),
    pdb_name: str,
    length: str,
    max_iter: str,
    method: str,
    gpu: str | None,
    alpha: float,
    batch_size: str | None,
    db: AsyncSession,
):
    item_input = PipelineItem(
        class_id=1,
        length=int(length),
        method_id=int(method),
        max_iter=int(max_iter),
        alpha=alpha,
        gpu=bool(gpu),
        batch_size=int(batch_size),
        receptor=pdb_name if pdb_name != None else "none",
        status="working...",
    )
=======
    db: AsyncSession,
    class_id: int | None = None,
    pdb_name: str | None = None,
    length: str | None = None,
    max_iter: str | None = None,
    method: str | None = None,
    gpu: str | None = None,
    alpha: float | None = None,
    batch_size: str | None = None,
    heavy: str | None = None,
    light: str | None = None,
    antigen: str | None = None,
    name: str | None = None,
):
    if class_id == 1:
        item_input = PipelineItem(
            class_id=class_id,
            length=int(length),
            method_id=int(method),
            max_iter=int(max_iter),
            alpha=float(alpha),
            gpu=bool(gpu),
            batch_size=int(batch_size),
            receptor=pdb_name if pdb_name != None else "none",
            status="working...",
        )
    elif class_id == 2:
        item_input = PipelineItem(
            class_id=class_id, heavy=heavy, light=light, antigen=antigen, name=name
        )
>>>>>>> e2c2703 (update)
    return await crud_pipeline.create_item(db=db, item=item_input)


async def check_dir_name(pipeline_id: int, db: AsyncSession):
    dir_name = await crud_pipeline.check_directory_name(pipeline_id, db)
    if dir_name == None:
        dir_name = await crud_pipeline.create_new_directory(pipeline_id, db)
    return dir_name


async def get_pipeline_info(pipeline_id: int, db: AsyncSession):
    result = await crud_pipeline.get_item(pipeline_id, db)
    method_option = ""
    if result.method_id == 1:
        method_option = "ucb"
    elif result.method_id == 2:
        method_option = "beta"
    return {
        "data": {
            "result": {
                "id": result.id,
                "created_at": result.created_at.replace(tzinfo=pytz.UTC)
                .astimezone(pytz.timezone("Asia/Seoul"))
                .strftime("%Y-%m-%d %H:%M:%S"),
                "ligand": "",
                "receptor": Path(result.receptor).stem,
                "method_id": method_option,
                "batch_size": result.batch_size,
                "length": result.length,
                "alpha": result.alpha,
                "class": "peptide",
            }
        }
    }


async def get_result(pipeline_id: int, db: AsyncSession):
    top10 = await crud_result.get_result_items(pipeline_id, db)
    return {
        "data": {
            "result_list": [
                {
                    "iter": result.iter,
                    "score": result.score,
                    "sequence": result.sequence,
                    "created_at": result.created_at.replace(tzinfo=pytz.UTC)
                    .astimezone(pytz.timezone("Asia/Seoul"))
                    .strftime("%Y-%m-%d %H:%M:%S"),
                }
                for result in top10["result"]
            ],
        }
    }


async def get_result_batch(pipeline_id: int, batch: int, db: AsyncSession):
    batch_result = await crud_result.get_result_items_batch(pipeline_id, batch, db)
    return [
        {
            "sequence": batch.sequence,
            "score": batch.score,
            "iter": batch.iter,
            "created_at": batch.created_at.replace(tzinfo=pytz.UTC)
            .astimezone(pytz.timezone("Asia/Seoul"))
            .strftime("%Y-%m-%d %H:%M:%S"),
        }
        for batch in batch_result
    ]


async def get_progress(pipline_id: int, db: AsyncSession):
    max_iter = await crud_pipeline.get_max_iter(pipline_id, db)
    result = await crud_result.get_last_iter(pipline_id, db)
    return round(result / max_iter, 4)


async def run_pipeline_loop(
    pdb_name: str,
    pdb_content: any,
    length: str,
    max_iter: str,
    method: str,
    gpu: str | None,
    alpha: float,
    batch_size: str,
    db: AsyncSession,
):
    bclient = BanditModelClient(burl)
    fclient = FoldModelClient(furl)
    dclient = DockModelClient(durl)

    pipeline_id = await init_new_pipeline(
<<<<<<< HEAD
        pdb_name, length, max_iter, method, gpu, alpha, batch_size, db
=======
        class_id=1,
        pdb_name=pdb_name,
        length=length,
        max_iter=max_iter,
        method=method,
        gpu=gpu,
        alpha=alpha,
        batch_size=batch_size,
        db=db,
>>>>>>> e2c2703 (update)
    )
    dir_name = await check_dir_name(pipeline_id, db)
    status_new = await dep_status.init_status(pipeline_id, db)

    upload_result = await dclient.upload(
        data={
            "pipeline_id": pipeline_id,
            "dir_name": dir_name,
        },
        files={"pdb": (pdb_name, BytesIO(pdb_content))},
    )
    init_bandit = await bclient.start(
        {
            # "pdb": pdb,
            "length": int(length),
            "max_iter": int(max_iter),
            "method": int(method),
            "alpha": float(alpha),
            "batch_size": int(batch_size),
        }
    )

    fasta_list = init_bandit["initial_fastas"]
    param = init_bandit["param"]
    iter = await dep_status.check_status_iter(pipeline_id, db)

    while iter <= int(max_iter):
        await dep_status.update_status_step(pipeline_id, 1, db)
        await fclient.start(
            {
                "pipeline_id": pipeline_id,
                "dir_name": dir_name,
                "iter": iter,
                "fasta_list": fasta_list,
            }
        )
        while True:
            step_now = await dep_status.check_status_step(pipeline_id, db)
            if step_now == 2:
                break
            await asyncio.sleep(1)

        await dclient.start(
            {
                "pipeline_id": pipeline_id,
                "dir_name": dir_name,
                "receptor_pdb": pdb_name,
                "iter": iter,
                "batch_size": int(batch_size),
            }
        )
        while True:
            step_now = await dep_status.check_status_step(pipeline_id, db)
            if step_now == 3:
                break
            await asyncio.sleep(1)

        update_task = await bclient.update(
            {
                "pipeline_id": pipeline_id,
                "method": int(method),
                "alpha": alpha,
                "length": length,
                "param": param,
                "iter": iter,
            }
        )

        fasta_list = update_task["new_fasta_list"]
        param = update_task["new_param"]
        await dep_status.update_status_iter(pipeline_id, iter + 1, db)
        iter = await dep_status.check_status_iter(pipeline_id, db)

    finish_pipeline_loop(pipeline_id, db)
    return await get_pipeline_info(pipeline_id, db)


<<<<<<< HEAD
=======
async def concat_minibody(
    heavy: str,
    light: str,
    antigen: str,
    name: str,
    db: AsyncSession,
):
    fclient = FoldModelClient(furl)

    pipeline_id = await init_new_pipeline(
        class_id=2, heavy=heavy, light=light, antigen=antigen, name=name, db=db
    )

    dir_name = await check_dir_name(pipeline_id, db)

    await fclient.start_multi(
        {
            "pipeline_id": pipeline_id,
            "heavy": heavy,
            "light": light,
            "antigen": antigen,
            "dir_name": dir_name,
        }
    )


>>>>>>> e2c2703 (update)
async def finish_pipeline_loop(pipeline_id: int, db: AsyncSession):
    return await crud_pipeline.finish_item(pipeline_id, db)