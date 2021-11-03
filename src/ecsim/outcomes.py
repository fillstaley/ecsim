"""...

...

"""


from collections import UserList
from logging import getLogger
from typing import Optional

from pandas import DataFrame


class Outcome:
    """Stores the results of election and determines the winner.

    Attributes
    ----------
    results : DataFrame
        The results of an election, ie. vote counts for each candidate
    totals : DataFrame
        The total electors won for each candidate, as well as their total vote counts
    winner : str
        The winner of the election

    """

    __slots__ = ["results", "totals", "winner", "_logger"]

    def __init__(self, results: DataFrame) -> None:
        """Determines the winner of the results of an election.

        Parameters
        ----------
        results : DataFrame
            The results of an election, ie. vote counts for each candidate:
            the rows are states and the columns are candidates.

        """
        self._logger = getLogger(__name__ + f".{self.__class__.__name__}")
        self.results = results

        self._logger.debug("Tallying the results of the election")
        self.totals = self._tally_results()
        self._logger.debug("Finished tallying the results")

        self._logger.debug("Determining the winner of the election")
        self.winner = self.get_winner()
        self._logger.info(self)

    def __str__(self) -> str:
        # TODO: fix the winner string, make it more readable, remove the word 'Votes'
        winner = self.winner
        electors = self.totals["Electors"][winner]
        return f"{winner} won the election with {electors} electors"

    @property
    def majority_electors(self) -> int:
        """The majority threshold of electors for a candidate winning an election."""
        return sum(self.results["Electors"]) // 2 + 1

    def get_winner(self, state: Optional[str] = None) -> str:
        """Determines which candidate won an election.

        Parameters
        ----------
        state : str, optional
            The name of a state

        Returns
        -------
        str
            The winner of an election, or the winner of a particular state if given

        """
        if state is not None:
            return self.results.loc[state].idxmax()

        for candidate, electors in self.totals["Electors"].items():
            if electors >= self.majority_electors:
                return candidate
        return "No winner!"

    def _tally_results(self) -> DataFrame:
        """Adds up all the electors and votes each candidate received."""
        totals = DataFrame(
            0, index=self.results.columns[:-1], columns=["Electors", "Votes"]
        )

        for state, electors in self.results["Electors"].iteritems():
            winner = self.get_winner(state)
            self._logger.debug(f"{winner} wins {electors} electors from {state}")
            totals["Electors"][winner] += electors
        self._logger.debug("Getting total vote count for each candidate")
        totals["Votes"] = self.results.sum()[:-1]

        return totals


class OutcomeList(UserList):
    @property
    def get_summary(self):
        summary = DataFrame(
            0,
            index=self[0].totals.index,
            columns=["Electoral College Wins", "Popular Vote Wins"],
            dtype=int,
        )

        for outcome in self:
            summary["Electoral College Wins"][outcome.winner] += 1
            summary["Popular Vote Wins"][outcome.totals["Votes"].idxmax()] += 1
        return summary
