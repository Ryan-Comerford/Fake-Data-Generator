# MythosMaker

This is a python library to generate fake data for testing purposes. This mainly uses the faker, sqlalchemy, sqlite, and multiprocessing libraries to generate fake data objects in multiple processes to speed up performance and generate large amounts of data.

# How to Use

```python
from MythosMaker import run_generator
```

# Arguments (with = as the default values)

sql_models_path (i.e. the path to your sqlalchemy models to be used).
database_uri='sqlite:///database.db' (i.e. the name of your database to be persisted).
number_of_processes=5 (i.e. the number of processes, keep in mind the more you add the more overhead on the system).
number_of_records=1000 (i.e. the number of records to be persisted).

# Additional Notes

This framework will only pickup tables defined by classes in the sqlalchemy models files.
Default values will be filled in depending on your data type.
It is best to overestimate the size of your columns.
Do not add too many processes.
The more records you add the more it can be overloaded.