"""

...

"""


from io import BytesIO
from logging import getLogger
from pkgutil import get_data

from pandas import DataFrame, read_csv


__all__ = ["load_census_data", "load_election_data"]


logger = getLogger(__name__)


def load_census_data() -> DataFrame:
    """Loads decennial Census data from a csv file."""
    census_path = "_data/Census.csv"
    logger.debug(f"Loading census data from {census_path}")
    return _load_data(census_path, index="Name")


def load_election_data(year: int) -> DataFrame:
    """Loads election data from a csv file.

    Parameters
    ----------
    year : int
        A presidential election year (ie. multiple of 4)

    Returns
    -------
    DataFrame
        Votes cast in the election, rows are states and columns are candidates

    """
    election_path = f"_data/Election{year}.csv"
    logger.debug(f"Loading election data from file: {election_path}")
    return _load_data(election_path, index="Name").astype(int)


def _load_data(path, index: str = "Name") -> DataFrame:
    return read_csv(BytesIO(get_data(__name__, path)), index_col=index)
