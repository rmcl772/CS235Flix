import pytest
from os import getcwd, path
from CS235Flix.adapters import memory_repository
from dotenv import load_dotenv


@pytest.fixture
def repo():
    load_dotenv()

    data_dir = path.join(getcwd(), "tests", "data")
    mem_repo = memory_repository.init_repo(data_dir)
    memory_repository.repo_instance = mem_repo

    return mem_repo
