import os
from box.exceptions import BoxValueError
import yaml
from textSummaryGenerator.logging import logger
from box import ConfigBox
from pathlib import Path
from typing import Any

try:
    from ensure import ensure_annotations
except Exception:
    # ensure==1.0.2 is not compatible with Python 3.12+.
    # Fallback keeps runtime behavior while skipping annotation enforcement.
    def ensure_annotations(func):
        return func

# Explaination of ensure_annotations and ConfigBox can be found in the research folder in trials.ipynb file.
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a yaml file and returns a ConfigBox object.
    
    Args:
        path_to_yaml (Path): Path to the yaml file.
        
    Raises:
        ValueError: If the yaml file is empty.
        e: empty file.
        
    Returns:
        ConfigBox: ConfigBox type.
    """ 
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates a list of directories.
    
    Args:
        path_to_directories (list): List of paths to directories.
        ignore_log (bool): ignore if multiiple directories is to be created. Defaults to false.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
            
@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

