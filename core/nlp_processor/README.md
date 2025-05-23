

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
| Bag-of-Words          | Extracts bag-of-words features from the HTML                              | `bag_of_words`           |
