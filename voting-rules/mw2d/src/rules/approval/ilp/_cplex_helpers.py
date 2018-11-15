import cplex


def print_all_variables(problem):
    # type: (cplex.Cplex) -> None
    x = problem.solution.get_values()
    for j in range(problem.variables.get_num()):
        print("{0} = {1}".format(problem.variables.get_names(j), x[j]))
    print "--------------------"
    print ""
    pass


def add_boolean_variable(problem, name, obj):
    # type: (cplex.Cplex, str, float) -> None
    problem.variables.add(
        obj=[obj],
        lb=[0.0],
        ub=[1.0],
        names=[name],
        types=[problem.variables.type.integer]
    )
    pass


def get_committee_from_boolean_variable_names(
        problem,
        number_of_candidates,
        candidate_to_var_name_fun,
        var_name_to_candidate_fun):
    # type: (cplex.Cplex, int, callable, callable) -> list[int]
    var_names = [candidate_to_var_name_fun(c=c) for c in range(number_of_candidates)]
    var_values = problem.solution.get_values(var_names)
    committee = []
    for name, value in zip(var_names, var_values):
        if value > 0.0:
            committee.append(var_name_to_candidate_fun(name))
    return committee


# TODO remove
def setObjectiveFunction(problem, variables_names, variables_coefficients, maximize):
    # type: (cplex.Cplex, list[str], list[float], bool) -> None
    problem.objective.set_name("objective123")

    # zero out objective function
    number_of_variables_in_default_objective = len(problem.objective.get_linear())
    problem.objective.set_linear([(idx, 0.0) for idx in range(number_of_variables_in_default_objective)])

    # set objective to epsilon
    problem.objective.set_linear(zip(variables_names, variables_coefficients))

    sense = problem.objective.sense.maximize if maximize else problem.objective.sense.minimize
    problem.objective.set_sense(sense)

    pass


def write(c, file_name):
    # type: (cplex.Cplex, str) -> None
    import pathlib2
    # pathlib2.Path("/home/pbatko/src/code-misc/python/voting-rules/piotr/lp-files/").mkdir(parents=False, exist_ok=True)
    # c.write("/home/pbatko/src/code-misc/python/voting-rules/piotr/lp-files/" + file_name)
    # exit(1)
    pass


def suppress_output(problem, log=True, results=True, warning=False, error=False):
    problem.set_log_stream(None) if log else None
    problem.set_results_stream(None) if results else None
    problem.set_warning_stream(None) if warning else None
    problem.set_error_stream(None) if error else None
    pass
