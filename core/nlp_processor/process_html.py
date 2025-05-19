import asyncio

from core.database_logic.database_client import DatabaseClient
from core.nlp_processor.processing_job_runner import ProcessingJobRunner

if __name__ == "__main__":
    runner = ProcessingJobRunner(
        db_client=DatabaseClient()
    )
    asyncio.run(runner.run_all())