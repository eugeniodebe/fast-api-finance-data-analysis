import re
import math


from sqlalchemy.inspection import inspect

def filter_valid_columns(data: dict, model) -> dict:
    """
    Filter out keys from the data that are not valid columns in the ORM model.
    """
    valid_columns = {column.key for column in inspect(model).mapper.column_attrs}
    return {key: value for key, value in data.items() if key in valid_columns}


def replace_nan_with_none(data_dict):
    """Replaces NaN values in the dictionary with None."""
    return {key: (None if isinstance(value, float) and math.isnan(value) else value) for key, value in data_dict.items()}

def to_snake_case(sentence_str):
    """Convert a sentence-like string to snake_case."""
    # Split by spaces or other non-word characters and join with underscores
    words = re.split(r'[\s]+', sentence_str.strip())
    # Convert words to lowercase and join with underscores
    return '_'.join(word.lower() for word in words if word)

def convert_keys_to_snake_case(original_dict):
    """Convert all keys in the dictionary to snake_case."""
    return {to_snake_case(key): value for key, value in original_dict.items()}