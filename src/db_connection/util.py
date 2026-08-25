import os

"""
File for the engine Singleton
"""

def get_env_var(name):
    var=os.getenv(name)
    if not var:
        raise ValueError(f"Environement variable {name} is empty")
    return var