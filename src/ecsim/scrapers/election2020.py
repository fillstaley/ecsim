import logging

from ecsim.scrapers.base import get_table, state_names


logger = logging.getLogger(__name__)


year = "2020"


def scrape_data():
    global year
    logger.debug(f"Getting data for the {year} election")
    data = get_table(year=year, match="(State or)")

    return clean_data(data)


def clean_data(data):
    # extract certain columns and then rename the columns
    data = data.iloc[:-2, [0, 1, 4, 7, 10, 13, 16, 19]]

    data.columns = [
        "State",
        "Biden (Democratic) Votes",
        "Trump (Republican) Votes",
        "Jorgensen (Libertarian) Votes",
        "Hawkins (Green) Votes",
        "Other Votes",
        "Margin Votes",
        "Total Votes",
    ]

    # clean the data
    for row in data.index:
        for col in data.columns[1:]:
            # remove commas from the entries
            data.loc[row, col] = data.loc[row, col].replace(",", "")
            # replace the unicode minus sign \u2212 with a dash
            data.loc[row, col] = data.loc[row, col].replace("\u2212", "-")
            # set non-numeric entries to 0
            if not data.loc[row, col].lstrip("-").isnumeric():
                data.loc[row, col] = 0

    # drop Maine districts information
    data.drop(index=[20, 21], inplace=True)
    # drop Nebraska districts information
    data.drop(index=[30, 31, 32], inplace=True)

    # change index names
    data["State"] = state_names
    data.rename(columns={"State": "Name"}, inplace=True)
    data.set_index("Name", inplace=True)

    return data


# if __name__ == "__main__":
#     data = scrape_election_results()
#     print(data)
