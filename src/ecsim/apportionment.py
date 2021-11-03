from numpy import ceil, floor, sqrt


# TODO: improve this implementation
# TODO: add documentation for apportionment methods
class ApportionmentMethod:
    def __init__(self, mean_) -> None:
        self._mean = mean_

    def __call__(self, num_representatives: int, states):
        divisor = sum(states.iloc[:, 0]) / num_representatives
        for state, population in states.iloc[:, 0].iteritems():
            quotient = population / divisor
            states.loc[state, "Representatives"] = self.round(quotient)

    def round(self, x):
        return floor(x) if x < self._mean(x) else ceil(x)


webster = ApportionmentMethod(lambda x: (floor(x) + ceil(x)) / 2)

huntington_hill = ApportionmentMethod(lambda x: sqrt(floor(x) * ceil(x)))

# Apportionment methods take as an input a mapping and a number, the method then
# apportions the number (whatever it represents) among the keys of the mapping
# in proportion to their corresponding values. This requires a divisor, a round
# method, and a check. The divisor is what to divide the values by to get a quotient,
# the round method then rounds the quotient up or down, and the check makes sure
# that the total number apportioned is correct and determines what to do if its not.
# The return of the method is a mapping with the same keys, but the values are the
# apportioned amounts.
