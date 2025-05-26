

## Terminology

### Overall
- **analysis family/family**: A category of jobs that share a general behavior or structure
    - Each family has one corresponding table
- **Template Group**: An optional subdivision of an analysis family that shares some of the same operations
    - These have no representation in tables, but are used to organize functions and queries and reduce redundancy
- **job type/type**: A specific analysis being done, e.g. counting `<a>` tags
    - Within each table, each job type has a corresponding enum value
- **job**: An individual process job that processes one attribute of a URL or its HTML
    - Within each table, a job for a URL has at least one corresponding row
    - In cases where a job was run but returned no results, a row is still created but with a value of `NULL`
- **set**: A group of jobs for a single URL
    - Has no tabular representation; refers to all jobs performed on a single URL at a given time
    - All jobs within a set are uploaded to the database at the same time for that URL
    - The jobs in a set are determined by queries
- **run**: An execution of all available sets

### Queries

- **Global check**: Determines whether any URLs in the database are missing results for a specific job type.
  - Used to decide whether to include that job type in the run.
- **Per-URL flag check**: Checks whether a given job type has already been performed for a specific URL.
   - Only performed in a given run if the global check indicates that the job type is still pending for at least one URL.

  
## Families

| Family                | Description                                                              | Associated Table         |
|-----------------------|--------------------------------------------------------------------------|--------------------------|
| URL Component         | Extracts information from the URL, such as scheme, domain, and path      | `url_components`         |
| HTML Content Metrics  | Extracts integer-based metrics, like number of proper nouns or locations | `html_content_metrics`   |
| HTML Metadata         | Extracts metadata like title, description, and keywords from the HTML    | `html_metadata`          |
| Bag-of-Words          | Extracts bag-of-words features from the HTML                             | `bag_of_words`           |
| Bag-of-Words by type | Extracts bag-of-words features from the HTML, subdividing by HTML type   | `bag_of_words_by_type`   |

## Adding a new Job

Each job is dynamically incorporated into the existing workflow. To ensure a job is properly incorporated, the following must be done:

### (A) Add a new family, if needed

#### (I) Add a new family enum value
1. Append a new enum value to the `FamilyType` enum in `core/nlp_processor/families/enums.py`
2. Add a new job type enum class to `core/nlp_processor/jobs/enums.py`, inheriting from `JobTypeEnumBase`

#### (II) Add a table and SQLAlchemy model
1. Using Alembic, create a new table in the database
2. Create a new SQLAlchemy model in `core/nlp_processor/families/registry/models.py`, inheriting from `FamilyModelBase`

#### (III) Create a Job Result Class 

1. Create a new directory in `core/nlp_processor/jobs/result/implementations`
2. Within the new directory:
  3. Create a new `core.py`, inheriting from `JobResultBase`
  4. Add any supporting classes as needed in separate files 

#### (IV) Create a new Job Result Mapper

1. In `core/nlp_processor/jobs/mapper`, in either the `direct` or `lookup` subdirectories:
  2. Create a new `factory.py` or `factories.py` file, or add to an existing one, if needed
  3. Add a new entry to the `implementations.py` file, inheriting from the associated `base.py` and `protocol.py`

#### (V) Add a new family registry entry
1. Add a new entry to `core/nlp_processor/families/registry/instances.py` that connects the family enum type, the SQLAlchemy model, the job result class, and the job result mapper

#### (VI) Add a new job type registry file
1. Create a new file in `core/nlp_processor/jobs/registry/instances/{family_name}.py`
2. Within the new file, create a new list that will encompass all registry entries for that family
3. Import that list into `core/nlp_processor/jobs/registry/instances/all.py` and add it to the `JOB_REGISTRY`

#### (VII) Add a new job identifier
1. Add a new subclass of `JobIdentifierBase` to `core/nlp_processor/jobs/identifiers/implementations.py`

#### (VIII) Add a new job processor folder and template
1. Create a new directory in `core/nlp_processor/jobs/processors/families/`
2. Create a new `_template.py` file in the new directory

### (B) Add a new job enum value

1. Add a new entry to the associated job type enum in `core/nlp_processor/jobs/enums.py`

### (C) Add a new processor

1. In the `core/nlp_processor/jobs/processors/families/{family_name}` directory:
  2. Create a new `factory.py` or `factories.py` file in the new directory, if needed. 
  3. Create a new `implementations.py` file in the new directory

### (D) Add a new job registry entry
1. In the `core/nlp_processor/jobs/registry/instances/{family_name}.py` file:
  2. Add a new entry to the `JOB_REGISTRY`, specifying the job identifier and processor
