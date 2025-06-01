"""
Process URLs for analysis information, one URL at a time
"""

import asyncio

from src.db.client import DatabaseClient
from src.nlp_processor.jobs.registry.instances.all import JOB_REGISTRY
from src.nlp_processor.run_manager.core import RunManager

if __name__ == "__main__":
    run_manager = RunManager(
        db_client=DatabaseClient()
    )
    job_ids = JOB_REGISTRY.get_identifiers()
    asyncio.run(run_manager.run(job_ids))
