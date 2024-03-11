import importlib
import random
from sqlalchemy import create_engine, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
import faker
import multiprocessing
import string
from datetime import datetime
import numpy as np
from ..utils.string_utils import *

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

sampled_foreign_key_values = {}

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
                        referenced_column = list(column.foreign_keys)[0].column
                        referenced_table_name = referenced_column.table.name
                        
                        if referenced_table_name in sampled_foreign_key_values:
                            referenced_values = sampled_foreign_key_values[referenced_table_name]
                        else:
                            referenced_values = session.query(referenced_column).order_by(func.random()).limit(100).all()
                            sampled_foreign_key_values[referenced_table_name] = referenced_values
                        if referenced_values:
                            fake_fk_value = random.choice(referenced_values)[0]
                        else:
                            fake_fk_value = random.randint(1, number_of_records)
                        setattr(model_instance, column.name, fake_fk_value)
                    else:
                        if isinstance(column.type, Integer):
                            fake_int_value = random.randint(1, 1000000)
                            setattr(model_instance, column.name, fake_int_value)
                        elif isinstance(column.type, String):
                            for key, handler in column_handlers.items():
                                if key in column.name.lower():
                                    fake_str_value = handler(fake)
                                    break
                            else:
                                fake_str_value = create_default(fake)
                            setattr(model_instance, column.name, fake_str_value)
                        elif isinstance(column.type, DateTime):
                            fake_dt_value = datetime.now()
                            setattr(model_instance, column.name, fake_dt_value)
                with lock:
                    session.add(model_instance)
    with lock:
        try:
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            print('NOTE: Bypassing error...Continuing the generation...')

def run_generator(sql_models_path, database_uri='sqlite:///database.db', number_of_processes=5, number_of_records=1000):
    create_db(sql_models_path, database_uri)

    lock = multiprocessing.Lock()
    processes = []
    for _ in range(number_of_processes):
        process = multiprocessing.Process(target=generate_data, args=(lock, sql_models_path, database_uri, number_of_records//number_of_processes))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()