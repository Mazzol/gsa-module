# -*- coding: utf-8 -*-
"""stochastic_evolutionary.py: Module containing functionalities to optimize
a given Latin Hypercube Design using an implementation of Enhanced Stochastic
Evolutionary Algorithm proposed by Jin, Chen, and Sudjianto (1). Details can
be found in (1) for the enhanced version and (2) for the original version.

**References**

 (1) R. Jin, W. Chen, and A. Sudjianto, "An Efficient Algorithm for Constructing
     Optimal Design of Computer Experiments," Proceedings of DETC'03, ASME 2003
     Design Engineering Technical Conferences and Computers and Information in
     Engineering Conference, Chicago, Illinois, Sept. 2-6, 2003.
 (2) Y.G. Saab and V.B. Rao, "Combinatorial Optimization by Stochastic
     Evolution," IEEE Transactions on Computer-Aided Design, vol. 10(4), 1981.
"""
import types
import math
import numpy as np
from . import objective_functions


__author__ = "Damar Wicaksono"


def pick_obj_function(obj_function: str) -> types.FunctionType:
    """Function to select by name the objective function to optimize

    :param obj_function: the name of the objective function
    :return: the objective function (FunctionType data type)
    """
    if obj_function == "w2_discrepancy":
        return objective_functions.w2_discrepancy
    else:
        raise TypeError("Unsupported objective function")


def init_threshold(dm: np.ndarray,
                   obj_func: types.FunctionType,
                   multiplier: float = 0.005) -> float:
    """Calculate the initial threshold as recommended in the article

    The initial threshold is obtained by multiplying the objective function of
    the initial design by a very small multiplier to get a small threshold.

    :param dm: the initial design matrix
    :param obj_func: the objective function (FunctionType data type)
    :param multiplier: the multiplier to have a very small value of threshold
        based on the initial design's objective function (default = 0.005)
    :return: the initial threshold
    """
    return multiplier*obj_func(dm)


def num_candidate(n: int) -> int:
    """Calculate the number of candidates from perturbing the current design

    Recommended in the article is the maximum number of pair combination from a
    given column divided by a factor of 5.

    :param n: the number of elements to be permuted
    :return: the number of candidates from perturbing the current design
        column-wise
    """
    pairs = math.factorial(n) / math.factorial(n-2) / math.factorial(2)
    fac = 5 # The factor recommended in the article
    return int(pairs/fac)


def max_inner(n: int, k: int) -> int:
    """Calculate the maximum number of inner iterations

    :math:`\frac{2 \times n_e \times k}{J}`

    :param n: the number of samples in the design
    :param k: the number of design dimension
    :return: the maximum number of inner iterations/loop
    """
    pairs = math.factorial(n) / math.factorial(n-2) / math.factorial(2)
    return int(2*pairs*k/num_candidate(n))


def perturb(dm: np.ndarray,
            num_dimension: int,
            j: int,
            obj_func: types.FunctionType) -> np.ndarray:
    """Create new configuration of a design matrix according to ESE algorithm

    According to the algorithm, a distinct `num_candidate` designs have to be
    generated from the current design by carrying out a column-wise perturbation
    on a given column `num_dimension`. The best design according to the select
    `obj_function` will be selected as the "perturbed" design

    :param dm: the current design matrix
    :param num_dimension: the column of design matrix to be perturbed
    :param j: the number of distinct candidates to be generated
    :param obj_func: the select objective function
    :return: the perturbed state of the current design
    """
    import itertools

    # Create pairs of all possible combination
    n = dm.shape[0]
    pairs = list(itertools.combinations([_ for _ in range(n)], 2))
    # Create random choices for the pair of perturbation, w/o replacement
    rand_choices = np.random.choice(len(pairs), j, replace=False)
    obj_func_current = np.inf
    dm_current = dm
    for i in rand_choices:
        dm_try = dm.copy() # Always perturb from the design passed in argument
        # Do column-wise operation in a given column 'num_dimension'
        dm_try[pairs[i][0], num_dimension] = dm[pairs[i][1], num_dimension]
        dm_try[pairs[i][1], num_dimension] = dm[pairs[i][0], num_dimension]
        obj_func_try = obj_func(dm_try)
        if obj_func_try < obj_func_current:
            # Select the best trial from all the perturbation trials
            obj_func_current = obj_func_try
            dm_current = dm_try

    return obj_func_current, dm_current


def optimize(dm: np.ndarray,
             obj_function: str = "w2_discrepancy",
             threshold_init: float = -1.0,
             j: int = 0,
             m: int = 0,
             max_outer: int = 100,
             improving_params: list = [0.1, 0.8],
             exploring_params: list = [0.1, 0.8, 0.9, 0.7]):
    """

    :param dm: the initial design matrix
    :param obj_function: the objective function used in the optimization
    :param threshold_init: the initial threshold, if negative calculate from
        the recommended value
    :param j: the number of candidates obtained by perturbing current design,
        0 or less means calculate from the recommended value
    :param m: the maximum number of inner iterations, 0 or less means calculate
        from the recommended value
    :param max_outer: the maximum number of outer iterations, served as the
        stopping criterion for the optimization algorithm
    :param improving_params: The 2 parameters used in improving process phase
        (1) the cut-off value to decrease the threshold
        (2) the multiplier to decrease or increase the threshold
    :param exploring_params: The 4 parameters used in exploring process phase
        (1) the cut-off value of acceptance to start increasing the threshold
        (2) the cut-off value of acceptance to start decreasing the threshold
        (3) the cooling multiplier for the threshold
        (4) the warming multiplier for the threshold
    :return: a collection of obj_function evolution and best design
    """
    # Initialization of Outer Iteration
    n = dm.shape[0]     # number of samples
    k = dm.shape[1]     # number of dimension
    obj_func = pick_obj_function(obj_function)  # Choose objective function
    if threshold_init < 0.0:
        threshold = init_threshold(dm, obj_func)   # Initial threshold
    else:
        threshold = threshold_init
    if j <= 0:
        j = num_candidate(n)    # number of candidates in perturbation process
    if m <= 0:
        m = max_inner(n, k)     # maximum number of inner iterations

    dm_current = dm.copy()
    flag_imp = False            # Outer iteration found improved solution flag

    obj_func_best = obj_func(dm)
    # Begin Outer Iteration
    outer = 0
    while outer < max_outer:
        # Initialization of Inner Iteration
        n_accepted = 0              # number of accepted trial
        n_improved = 0              # number of improved trial

        # Begin Inner Iteration
        for inner in range(m):
            obj_func_current = obj_func(dm_current)
            # Perturb current design
            obj_func_try, dm_try = perturb(dm, inner, j, obj_func)
            if (obj_func_try - obj_func_current) <= threshold * np.random.rand():
                # Accept solution
                dm_current = dm_try.copy()
                n_accepted += 1
                if obj_func_try < obj_func_best:
                    # Best solution found
                    dm_best = dm_current.copy()
                    n_improved += 1

    # Accept/Reject as Best Solution for convergence
    if (obj_func_best - obj_func(dm_best))/obj_func_best > 1e6:
        obj_func_best = obj_func(dm_best)
        flag_imp = True
        outer -= 1
    else:
        flag_imp = False
        outer += 1

    # Improve vs. Explore Phase
    # Threshold Update
    # Update Stopping Criteria

    return dm_try