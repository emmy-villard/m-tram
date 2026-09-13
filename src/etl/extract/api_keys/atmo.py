from util.env import get_env_var

env_variable_name = "ATMO_API_KEY"

def get_api_key():
    api_key = get_env_var(env_variable_name)
    if api_key == "":
        raise ValueError("Please export ATMO_API_KEY")
    return api_key