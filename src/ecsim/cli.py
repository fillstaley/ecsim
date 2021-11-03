"""Provides a CLI for simulating a US election.

...

"""

import click
from rich import print

from ecsim import *
from ecsim.scrapers import *


@click.group()
def main():
    ...


@main.command()
@click.option("-y", "--year", default=2020, show_default=True)
@click.option("-r", "--representatives", default=435, show_default=True)
@click.option("-u", "--uncertainty", default=0.0)
@click.option("-n", "--number", default=1)
def run(year, representatives, uncertainty, number):
    election = Election(year, representatives)
    results = OutcomeList()

    with click.progressbar(
        range(number), label=f"Simulating {number} elections"
    ) as bar:
        for _ in bar:
            results.append(election.simulate(uncertainty))

    # TODO: improve summary of the results, include popular vote wins
    print(results.get_summary)


@main.command()
@click.option("-o", "--output-dir", default="data", show_default=True)
def scrape(output_dir):
    scrape_census_data(output_dir)
    scrape_election_data(output_dir)
