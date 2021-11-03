from ecsim.scrapers import census
from ecsim.scrapers import election2004
from ecsim.scrapers import election2008
from ecsim.scrapers import election2012
from ecsim.scrapers import election2016
from ecsim.scrapers import election2020

__all_ = [
    "scrape_census_data",
    "scrape_election_data",
]


elections = [
    election2004,
    election2008,
    election2012,
    election2016,
    election2020,
]


def scrape_census_data(output_dir):
    census_data = census.scrape_data()
    census_data.to_csv(output_dir + "/" + "Census.csv")


def scrape_election_data(output_dir):
    global elections
    for election in elections:
        election_data = election.scrape_data()
        election_data.to_csv(output_dir + "/" + f"Election{election.year}.csv")
