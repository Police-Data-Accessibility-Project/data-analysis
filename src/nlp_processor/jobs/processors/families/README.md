# Processor Family Structure

Each subfolder in this directory represents a **processor family**, which handles a specific kind of job (e.g., `html_metadata`, `url_component`).

Each family typically contains:

- `_template.py`  
  Defines the abstract base class (template) for that family.  
  All implementations should inherit from this.

- `factory.py` or `factories.py`
  Contains one or more factory functions to generate one or more implementations based on dynamic parameters.

- `implementations.py`  
  Contains all concrete processor implementations. These may be defined directly or generated via the factory.

> 📌 Note: Not all families must include all three files — this is a general pattern, not a strict requirement.
