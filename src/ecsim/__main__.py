import ecsim as ec

election = ec.Election(2016)
outcome = election.simulate(2)

print(outcome)
print(outcome.totals)
