import os
import pytest

test_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(test_dir, "test_data")


@pytest.fixture
def test_directory():
    return test_dir


@pytest.fixture
def data_directory():
    return data_dir
