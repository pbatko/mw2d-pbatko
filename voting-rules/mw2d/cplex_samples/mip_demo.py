import cplex



def demo():


    # For example, if cpx is an instance of the class Cplex encapsulating a MIP (mixed
    # integer pr ogramming) pr oblem, you can specify which linear programming
    # algorithm is used for solving the r oot pr oblem and the node subpr oblems, like this:
    c = cplex.Cplex()

    start_algos = c.parameters.mip.strategy.startalgorithm.values
    sub_algos = c.parameters.mip.strategy.subalgorithm.values
    c.parameters.mip.strategy.startalgorithm.set(start_algos[0])
    c.parameters.mip.strategy.subalgorithm.set(sub_algos[0])


if __name__ == "__main__":
    demo()