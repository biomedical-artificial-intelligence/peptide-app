from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from model.psql import get_db
from api.dep import pipeline as dep_pipeline
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
)


router = APIRouter()


@router.get("/all")
async def page_pipeline(page: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    try:
        # skip = page * 10
        # pipeline_list = crud_pipeline.get_all_items(db, skip, 10)
        return await dep_pipeline.get_pipeline_items(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/run")
async def run_pipeline(
    bgtask: BackgroundTasks,
    # fasta: Optional[UploadFile] = File(None),
    # sequence: str = Form(...),
    class_id: Optional[str] = Form(None),
    pdb: Optional[UploadFile] = File(None),
    length: Optional[str] = Form(None),
    max_iter: Optional[str] = Form(None),
    method: Optional[str] = Form(None),
    gpu: Optional[str] = Form(None),
    alpha: Optional[str] = Form(None),
    batch_size: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    heavy: Optional[str] = Form(None),
    light: Optional[str] = Form(None),
    antigen: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        if class_id == None or class_id == "1":
            pdb_content = await pdb.read()
            bgtask.add_task(
                dep_pipeline.run_pipeline_loop,
                pdb.filename,
                pdb_content,
                length,
                max_iter,
                method,
                gpu,
                alpha,
                batch_size,
                db,
            )
            return {
                "message": "Pipeline Started for {} iteration".format(max_iter),
                "success": "ok",
            }
        elif class_id == "2":
            bgtask.add_task(
                dep_pipeline.concat_minibody,
                heavy,
                light,
                antigen,
                name,
                db,
            )
            return {
                "message": "Pipeline Started Multimer",
                "success": "ok",
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/info")
async def info_pipeline(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await dep_pipeline.get_pipeline_info(id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/result")
async def result_pipeline(
    id: int,
    batch: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    try:
        if batch == None:
            return await dep_pipeline.get_result(id, db)
        else:
            result_list = await dep_pipeline.get_result_batch(id, batch, db)
            return {"data": {"result_list": result_list}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/chart")
async def chart_pipeline_batch(
    id: int,
    batch: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        result_list = await dep_pipeline.get_result_batch(id, batch, db)
        return {"data": {"result_list": result_list}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/progress")
async def progress_pipeline(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await dep_pipeline.get_progress(id, db)
        return {"data": {"result": {"progress": result}}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e