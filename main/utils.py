 # for tests
from random import random
def generate_float(min_val, max_val, round_amt):
    return round(random() * (max_val-1) + min_val, round_amt)

def generate_site_url_name(name: str):
    return "-".join(name.lower().split())