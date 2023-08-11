from os.path import split, join, isfile

from dotenv import load_dotenv

env_path = join(split(split(__file__)[0])[0], 'env', '.env')


def load_from_env():
    global env_path
    if isfile(env_path):
        load_dotenv(env_path)
