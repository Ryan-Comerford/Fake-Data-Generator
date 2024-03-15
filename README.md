# Fake Data Generator

This is a python library to generate fake data for testing purposes

# Main Function + Args

To use import the following "from MythosMaker import run_generator"

The arguments are (with =default_value)
    1) sql_models_path (i.e. the path to your sqlalchemy models to be used)
    2) database_uri='sqlite:///database.db' (i.e. the name of your database to be persisted)
    3) number_of_processes=5 (i.e. the number of processes, keep in mind the more you add the more overhead on the system)
    4) number_of_records=1000 (i.e. the number of records to be persisted)

# Some Notes...

Default Strings will be filled in with a fake word from Faker library

This framework will only pickup tables defined by classes in the SQLAlchemy models files

It is best to overestimate the size of your columns

Do not add too many processes, 5 is recommended

The more records you add the more it can be overloaded