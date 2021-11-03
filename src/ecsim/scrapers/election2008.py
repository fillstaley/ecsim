import logging

from ecsim.scrapers.base import get_table, state_names


logger = logging.getLogger(__name__)


year = "2008"


def scrape_data():
    global year
    logger.debug(f"Getting data for the {year} election")
    data = get_table(year=year, match="(State/district)")

    return clean_data(data)


def clean_data(data):
    # extract certain columns and then rename the columns
    data = data.iloc[:-1, [0, 2, 5, 8, 11, 14, 17, 20, 23, 25]]

    data.columns = [
        "State",
        "Obama (Democratic) Votes",
        "McCain (Republican) Votes",
        "Nader (Independent) Votes",
        "Barr (Libertarian) Votes",
        "Baldwin (Constitution) Votes",
        "McKinney (Green) Votes",
        "Other Votes",
        "Margin Votes",
        "Total Votes",
    ]

    # TODO: maybe clean some of the entries and not others
    # col = "Margin Votes"
    # # clean the data
    # for row in data.index:
    #     # remove commas from the entries
    #     data.loc[row, col] = data.loc[row, col].replace(",", "")
    #     # replace the unicode minus sign \u2212 with a dash
    #     data.loc[row, col] = data.loc[row, col].replace("\u2212", "-")
    #     # set non-numeric entries to 0
    #     if not data.loc[row, col].lstrip("-").isnumeric():
    #         data.loc[row, col] = 0

    # drop Maine districts information
    data.drop(index=[20, 21], inplace=True)
    # drop Nebraska districts information
    data.drop(index=[30, 31, 32], inplace=True)

    # change index names
    data["State"] = state_names
    data.rename(columns={"State": "Name"}, inplace=True)
    data.set_index("Name", inplace=True)

    return data
