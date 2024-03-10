import importlib
import random
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
import faker
import multiprocessing
import string
from datetime import datetime
import numpy as np
from utils.string_utils import *

column_handlers = {
    'email': create_email,
    'username': create_username,
    'name': create_name,
    'gender': create_gender,
    'occupation': create_job,
    'job': create_job,
    'address': create_address
}

def create_db(sql_models_path, database_uri):
    models_module = importlib.import_module(sql_models_path)
    Base = getattr(models_module, "Base")
    engine = create_engine(database_uri, connect_args={'timeout': 30})
    Base.metadata.create_all(engine)

foreign_key_values = {}

def generate_data(lock, sql_models_path, database_uri, number_of_records):
    models_module = importlib.import_module(sql_models_path)
    engine = create_engine(database_uri, connect_args={'timeout': 30})
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    
    fake = faker.Faker(random.randint(1, 1000))
    
    for _ in range(number_of_records):
        for attr_name in dir(models_module):
            model_class = getattr(models_module, attr_name)
            if hasattr(model_class, '__table__'):
                model_instance = model_class()
                for column in model_class.__table__.columns:
                    if column.primary_key:
                        continue
                    elif column.foreign_keys:
                        fk = list(column.foreign_keys)[0]
                        pk_value = session.query(fk.column).order_by(func.random()).first()
                        fake_value = pk_value[0] if pk_value else 1
                        setattr(model_instance, column.name, fake_value)
                    else:
                        if isinstance(column.type, Integer):
                            fake_value = random.randint(1, 10000000)
                        elif isinstance(column.type, String):
                            for key, handler in column_handlers.items():
                                if key in column.name.lower():
                                    fake_value = handler(fake)
                                    break
                            else:
                                fake_value = create_default(fake)
                        elif isinstance(column.type, DateTime):
                            fake_value = datetime.now()
                        setattr(model_instance, column.name, fake_value)
                with lock:
                    session.add(model_instance)
    with lock:
        session.commit()
        session.close()

def run_generator(sql_models_path, database_uri, number_of_processes, number_of_records):
    create_db(sql_models_path, database_uri)

    lock = multiprocessing.Lock()
    processes = []
    for _ in range(number_of_processes):
        process = multiprocessing.Process(target=generate_data, args=(lock, sql_models_path, database_uri, number_of_records//number_of_processes))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()