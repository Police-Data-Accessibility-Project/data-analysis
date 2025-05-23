import asyncio

from core.database_logic.database_client import DatabaseClient
from core.nlp_processor.v2.globals import JOB_REGISTRY
from core.nlp_processor.v2.run_manager import RunManager

if __name__ == "__main__":
    run_manager = RunManager(
        db_client=DatabaseClient()
    )
    job_ids = JOB_REGISTRY.get_identifiers()
    asyncio.run(run_manager.run(job_ids))
