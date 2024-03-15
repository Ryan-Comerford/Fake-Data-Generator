from MythosMaker.generation.run_fake_generator import run_generator

if __name__ == '__main__':
    run_generator('models.sql_models', 'sqlite:///database.db', 10, 10000)
