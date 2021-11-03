"""A package of tools for simulating the US Electoral College.

...

"""


__version__ = "0.5.0"
__all__ = ["Election", "OutcomeList"]


import logging
from typing import Optional, Union

from pandas import DataFrame, Series
from numpy.random import default_rng

from ecsim.loaders import *
from ecsim.apportionment import *
from ecsim.outcomes import Outcome, OutcomeList


# TODO: improve logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(level=logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch.setFormatter(formatter)
logger.addHandler(ch)


_RANDOM_SEED = 713

SENATORS_PER_STATE: int = 2
"""The number of senators each state receives as specified in the US Constitution."""

DC_STATEHOOD: bool = False
"""Whether or not the District of Columbia is a state.

The seat of the US Government, the District of Columbia (DC), is not a state, nor
is it a part of any state. Until the ratification of the 23rd amendment, this meant
that it did not receive any electors in the vote for the president. With the adoption
of the 23rd Amendment in 1961, DC is granted as many electors it would have if it
were a state, but no more than the least populous state.
"""

census_data: DataFrame = load_census_data()
"""The (historical) US population data gathered with each decennial census."""


class Election:
    """Contains the data and method for simulating historical US elections.

    Attributes
    ----------
    year : int
        The year of the presidential election to simulate.
    union : DataFrame
        The historical election data used for the simulation.

    """

    __slots__ = [
        "year",
        "representatives",
        "apportionment_method",
        "union",
        "_logger",
        "_rng",
    ]

    def __init__(
        self,
        year: int,
        representatives: int = 435,
        apportionment_method: ApportionmentMethod = huntington_hill,
    ) -> None:
        """Initializes an election by loading Census data and election data.

        Parameters
        ----------
        year
            A presidential election year, must be a multiple of 4.
        representatives
            The total number of representatives in the House, by default 435,
            and must be at least equal to the number of states.
        apportionment_method
            The specific apportionment method to be used when apportioning
            representatives.

        """
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._rng = default_rng(_RANDOM_SEED)

        self.apportionment_method = apportionment_method

        if year % 4 != 0:
            raise ValueError(f"{year} is not an election year!")
        self.year = year

        self._logger.debug(f"Loading election data for {self.year}")
        self.union = load_election_data(self.year)

        number_states = len(self.union) - (
            1 if "District of Columbia" in self.union.index and not DC_STATEHOOD else 0
        )
        if representatives < number_states:
            raise ValueError("There are not enough representatives!")
        self.representatives = self.apportion_representatives(representatives)

    def get_electors(self, state: Optional[str] = None) -> Union[int, Series]:
        """Returns the number of electors for each state.

        Parameters
        ----------
        state : str, optional
            If present, computes the states electors from its number of representatives
            and the number of senators each state receives. Implements special logic
            for the District of Columbia, which is not a state but does receive electors.

        Returns
        -------
        Union[int, Series]
            If no state is given, then a pandas.Series is returned containing the number
            of electors each state receives.

        """
        if state is not None:
            if state == "District of Columbia" and not DC_STATEHOOD:
                # TODO: move this comment to a Note in the docstring
                # this is not techincally correct, but it is funcationally so,
                # ie. if the population of DC was so less than the least populous state
                # that it would be awarded 1 representative where the least populous
                # state would receive 2, then this equation will give too many electors
                # to DC, but this scenario seems implausible
                return (
                    self.representatives["Representatives"].min() + SENATORS_PER_STATE
                )
            else:
                return (
                    self.representatives["Representatives"][state] + SENATORS_PER_STATE
                )

        electors = Series(0, index=self.union.index, name="Electors", dtype=int)
        for state in electors.index:
            electors[state] = self.get_electors(state)
        return electors

    def apportion_representatives(self, number: int = 435) -> DataFrame:
        """Apportions some number of representatives among the states.

        Parameters
        ----------
        number : int, optional
            The number of representatives to be apportioned, by default 435

        Returns
        -------
        DataFrame
            Their is a row for every state and the number of representatives is stored
            in a column (called 'Representatives'), also contains a column with Census
            data used to compute the apportionment.

        """
        census_year = self.year // 10 * 10
        self._logger.debug(
            f"Initializing list of states with census data from {census_year}"
        )
        states = DataFrame(data=census_data[f"{census_year}"], dtype=int)
        states["Representatives"] = 0

        if "District of Columbia" in states.index and not DC_STATEHOOD:
            self._logger.debug(
                "Removing the District of Columbia because it is not a state"
            )
            states.drop("District of Columbia", inplace=True)

        self._logger.info(
            f"Apportioning {number} representatives among {len(states)} states"
        )
        global apportionment_method
        self.apportionment_method(number, states)
        self._logger.debug("Finished apportioning representatives")

        return states

    def simulate(self, percent_uncertainty: float = 0) -> Outcome:
        """Simulates a US presidential election.

        Parameters
        ----------
        percent_uncertainty : float, optional
            The percent magnitude of the random change in the results of the election,
            by default 0, and measured in percentage points (eg. an input of 2 means
            a 2% margin of change in the results)

        Returns
        -------
        Outcome
            The results of an election stored in an object

        """
        # self._logger.info("Simulating a US presidential election")
        self._logger.debug("Initializing election results from historical data")
        # TODO: fix the scrapers to remove the final two columns there
        results = self.union.iloc[:, :-2].copy()
        if percent_uncertainty:
            self._logger.info(
                f"Simulating an election with {percent_uncertainty:.1f}% uncertainty"
            )
            for candidate in results:
                for state, votes in results[candidate].iteritems():
                    bound = int(votes // 100 * percent_uncertainty)
                    results.loc[state, candidate] += self._rng.integers(
                        -bound, bound, endpoint=True
                    )

        else:
            self._logger.info("Simulating an election with no uncertainty")

        self._logger.debug("Getting electors for each state")
        results["Electors"] = self.get_electors()

        return Outcome(results)
