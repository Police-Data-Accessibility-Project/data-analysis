Processors are classes that perform a single task on a single URL

Processors are grouped by directory into families. Each directory contains the following files:

- `_template.py`  
    Defines the abstract base class (template) for that family.  
    All implementations should inherit from this.
    Each template should define an abstract method of the `process` method, specifying the specific return type
- `factory.py` or `factories.py`
    Contains one or more factory functions to generate one or more implementations based on dynamic parameters. This file is optional.
- `implementations.py`  
    Contains all concrete processor implementations. These may be defined directly or generated via the factory.