import faker
import random
import numpy as np
import string

def create_default(fake):
    fake_value = fake.word()
    
    return fake_value

def create_email(fake):
    domain_names = ['yahoo', 'aol', 'gmail', 'outlook', 'iCloud', 'Mail', 'GMX', 'ProtonMail', 'example', 'test', 'company']
    domains = ['.net', '.com', '.org']
    fake_name = fake.word() + fake.first_name().lower()
    fake_number = random.randint(100, 100000)
    fake_domain = random.choice(domain_names) + random.choice(domains)
    fake_value = f"{fake_name}{fake_number}@{fake_domain}"

    return fake_value

def create_address(fake):
    fake_value = fake.address()

    return fake_value

def create_username(fake):
    fake_name = fake.last_name().lower() 
    random_string_length = random.randint(3, 10)
    fake_letters = ''.join(random.choices(string.ascii_letters, k=random_string_length))
    fake_number = random.randint(100, 100000)
    fake_value = fake_name + fake_letters + str(fake_number)

    return fake_value

def create_gender(fake):
    fake_value = random.choice(['M', 'F'])

    return fake_value

def create_job(fake):
    fake_value = fake.job()

    return fake_value

def create_name(fake):
    fake_prefixes = np.random.choice(['', 'Dr. ','Prof '], p=[0.95, 0.03, 0.02])
    fake_suffix = np.random.choice(['', ' Jr.', ' Sr.', ' III'], p=[0.91, 0.05, 0.02, 0.02])
    fake_value = random.choice([fake_prefixes + fake.first_name_male() + ' ' + fake.first_name_male() + ' ' + fake.last_name() + fake_suffix, fake_prefixes + fake.first_name_female() + ' ' + fake.first_name_female() + ' ' + fake.last_name() + fake_suffix])

    return fake_value