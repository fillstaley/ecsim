from logging import getLogger

from pandas import read_html

# from ecsim._scrapers.base import state_names


logger = getLogger(__name__)


url = "https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population"


def scrape_data():
    global url
    logger.debug(f"Getting US Census data from {url}")
    [
        table1,  # census data for 1790--1860, also admitted years
        table2,  # enslaved population for 1790--1860
        table3,  # census data for 1870--1950
        table4,  # census data for 1960--2020
        *_,
    ] = read_html(url, match="Name", flavor="lxml")

    states, _ = clean_recent_data(table4)

    return states


def clean_recent_data(table):
    logger.debug("Separating states and territories")
    t_index = [2, 12, 37, 42, 48]
    territories = table.loc[t_index].copy()
    states = table.drop(t_index)
    # remove the total row
    states = states.drop(56)

    logger.debug("Cleaning territories data")
    territories.loc[37, "Name"] = territories.loc[37, "Name"][:-4].replace(",", "")
    territories.loc[37, "1960"] = territories.loc[37, "1960"][:-4].replace(",", "")
    territories.set_index("Name", inplace=True)

    logger.debug("Cleaning states data")
    states.set_index("Name", inplace=True)

    return states, territories


# if __name__ == "__main__":
#     data = scrape_data()
#     for foo, bar in zip(data.index, state_names):
#         print(f"Checking that {foo} is the same as {bar}")
#         assert foo == bar
