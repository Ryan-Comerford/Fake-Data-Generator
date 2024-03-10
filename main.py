from functions.generate_functions import run_generator

if __name__ == '__main__':
    run_generator('models.sql_models', 'sqlite:///db/database.db', 10, 100000)
