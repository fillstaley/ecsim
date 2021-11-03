Tutorial
========

...

Installation
------------

To get started, fist install the package using pip. The simplest option is to install
the published version from PyPi.

.. code-block:: shell

    pip install ecsim

But the package can also be installed directly from GitHub:

.. code-block:: shell

    pip install git+https://github.com/fillstaley/ecsim.git

Basic Usage
-----------

The package can be used through the command line directly using the `ecsim run` command.

.. code-block:: shell

    ecsim run --year 2016 --representatives 435 --uncertainty 5.0

This will run a simulation of the 2016 US presidential election with 435 representatives
(the current number) and 5% uncertainty in the vote outcomes for each state. This
percent uncertainty simply means that the historical vote outcomes for each candidate
are increased or decreased by the given percent.

Simulations can also be run by importing the package and creating an instance of an
`Election` object, giving the year and the number of representatives as initialization
arguments. Then calling the `simulate()` method will return the results of an election.

.. code-block:: python

    from ecsim import Election

    election = Election(year=2016, representatives=435)
    election.simulate(uncertainty=5.0)

The percent uncertainty can be specified as an argument for the `simulate()` method.
If no argument is given, then no uncertainty is assumed and the historical vote data
is used to "simulate" the election.
