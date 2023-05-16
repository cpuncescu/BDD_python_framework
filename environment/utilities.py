import os
import yaml


def yaml_file_load(filename):
    file = os.path.abspath(os.path.expanduser(filename))
    return yaml.safe_load(open(file))


yaml_file = yaml_file_load("tokens.yaml")
os.environ["book_token"] = yaml_file["tokens"]["simple_books_token"]