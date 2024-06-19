import pytest
from scripts.data_validation import validate_data

def test_data_validation():
    results = validate_data()
    assert results["success"] is True
