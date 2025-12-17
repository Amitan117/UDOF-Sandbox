"""
Data Registry Module

Contains dataset paths and expected files registry.
This module will be populated during migration from the runner.
"""

# TODO: Migrate dataset paths from runner
# TODO: Migrate expected files registry from runner


# Dataset paths registry
DATASET_PATHS = {
    # TODO: Populate with dataset paths from runner
    # Example structure:
    # 'bao': 'path/to/bao/data',
    # 'sne': 'path/to/sne/data',
    # etc.
}


# Expected files registry
EXPECTED_FILES = {
    # TODO: Populate with expected files for each dataset
    # Example structure:
    # 'bao': ['file1.csv', 'file2.npy'],
    # 'sne': ['file1.dat', 'file2.cov'],
    # etc.
}


def get_dataset_path(dataset_name: str) -> str:
    """
    Get the path for a given dataset.

    Args:
        dataset_name: Name of the dataset

    Returns:
        str: Path to the dataset

    Raises:
        KeyError: If dataset name is not found in registry
    """
    if dataset_name not in DATASET_PATHS:
        raise KeyError(f"Dataset '{dataset_name}' not found in registry")
    return DATASET_PATHS[dataset_name]


def get_expected_files(dataset_name: str) -> list:
    """
    Get the list of expected files for a given dataset.

    Args:
        dataset_name: Name of the dataset

    Returns:
        list: List of expected file names

    Raises:
        KeyError: If dataset name is not found in registry
    """
    if dataset_name not in EXPECTED_FILES:
        raise KeyError(f"Dataset '{dataset_name}' not found in registry")
    return EXPECTED_FILES[dataset_name]
