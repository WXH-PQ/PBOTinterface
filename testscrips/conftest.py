import time
import uuid
import pytest
from utils import  *

@pytest.fixture(scope='class')
def UUID():
    UUID = str(uuid.uuid4())
    return UUID

@pytest.fixture(scope='class')
def delay():
    print("休息30s")
    time.sleep(30)

@pytest.fixture(scope='class')
def t_start():
    t_start = date_format('now-1')
    return t_start

