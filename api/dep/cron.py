from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from model.psql import SessionLocal
import pexpect

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.on_event("startup")
@repeat_every(seconds=60 * 60)
async def periodic_task():
    child = pexpect.spawn(
        "scp -P {} {} {}@{}:{}/".format(hprt, fasta_path, husr, hurl, htgt)
    )
    child.expect(".*{}'s password:.*".format(hurl))
    child.sendline("{}".format(hpwd))
    child.expect(pexpect.EOF)
    child.close()
    print("Periodic task executed")