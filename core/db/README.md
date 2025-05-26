This repository contains all logic relating to the database. 


To start up the database, run:

```bash
$ docker-compose up -d
```

## Creating Family Models

Family models are incorporated into the existing nlp_processor logic. 
In order to be properly defined by the workflow, they must have the following attributes:
1. A `url_id` column properly pointing to the `urls` table.
2. A `type` column conforming to the expected `JobType` enum

In addition, each job must allow a default value for its value columns; even if null, this communicates to the database that this job has been run for that URL.