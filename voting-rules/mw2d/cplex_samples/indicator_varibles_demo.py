def cplex_demo():
    import cplex

    c = cplex.Cplex()

    c.objective.set_sense(c.objective.sense.maximize)

    c.variables.add(
        obj=[1.0, 1.0, 1.0, 1.0, -1.0],
        # lb=[0.0, 0.0],
        # ub=[10.0, 10.0],
        names=["x1", "x2", "b1", "b2", "b0"]
    )

    c.indicator_constraints.add(
        lin_expr=[
            ["b1"],
            [1.0]
        ],
        sense="G",
        rhs=1.0,
        indvar="b0",
        name="ind0",
        complemented=0,
        indtype=c.indicator_constraints.type_.if_
    )

    c.indicator_constraints.add(
        lin_expr=[
            ["x1", "x2"],
            [1.0, 3.0]
        ],
        sense="E",
        rhs=10.0,
        indvar="b1",
        name="ind1",
        complemented=0,
        indtype=c.indicator_constraints.type_.if_
    )

    c.indicator_constraints.add(
        lin_expr=[
            ["x1", "x2"],
            [2.0, 1.0]
        ],
        sense="E",
        rhs=10.0,
        indvar="b2",
        name="ind1",
        complemented=0,
        indtype=c.indicator_constraints.type_.if_
    )

    c.linear_constraints.add(
        lin_expr=[
            [
                ["b1", "b2"],
                [1.0, 1.0]
            ]
        ],
        senses=["E"],
        rhs=[1.0],
        names=["b1_or_b2"]
    )

    c.write("cplex_demo.lp")
    c.solve()

    x = c.solution.get_values(["x1", "x2", "b1", "b2", "b0"])

    print(x)
    # epsilon_value = problem.solution.get_values(epsilonName())
    #
    # new_voter_loads = []
    # for load_for_voter in vectorOfVoterLoads_names_indexedByVoter:
    #     load = 0.0
    #     for load_component_for_voter in load_for_voter:
    #         load += problem.solution.get_values(load_component_for_voter)
    #     new_voter_loads.append(load)

    # import cplex
    # c = cplex.Cplex()
    # indices = c.variables.add(names=["x1", "x2"])
    # c.indicator_constraints.add(
    #     indvar="x1",
    #     complemented=0,
    #     rhs=1.0,
    #     sense="G",
    #     lin_expr=cplex.SparsePair(ind=["x2"], val=[2.0]),
    #     name="ind1",
    #     indtype=c.indicator_constraints.type_.if_)
    pass


if __name__ == '__main__':
    cplex_demo()
