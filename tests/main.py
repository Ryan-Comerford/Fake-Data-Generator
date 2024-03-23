from MythosMaker import run_generator

if __name__ == '__main__':
    run_generator('models.sql_models', 'sqlite:///database.db', 5, 10000)
