"""
Utilities

A collection of utility functions

"""

__date__ = "2024-08-07"
__author__ = "James Sellers"

# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import toml
from pathlib import Path

# %% --------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def toml_creds():

    module_dir = Path(__file__).resolve().parent

    # Path to the creds.toml file relative to the module directory
    creds_path = module_dir / "creds.toml"

    # Open and read the creds.toml file
    with open(creds_path, "r") as f:
        creds = toml.load(f)

    return creds