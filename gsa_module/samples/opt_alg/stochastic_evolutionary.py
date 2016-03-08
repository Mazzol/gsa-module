# -*- coding: utf-8 -*-
"""stochastic_evolutionary.py: Module containing functionalities to optimize
a given Latin Hypercube Design using an implementation of Enhanced Stochastic
Evolutionary Algorithm proposed by Jin, Chen, and Sudjianto (1). Details can
be found in (1) and (2)

**References**

 (1) R. Jin, W. Chen, and A. Sudjianto, "An Efficient Algorithm for Constructing
     Optimal Design of Computer Experiments," Proceedings of DETC'03 ASME 2003
     Design Engineering Technical Conferences and Computers and Information in
     Engineering Conference, Chicago, Illinois, Sept. 2-6, 2003.
 (2) Y.G. Saab and V.B. Rao, "Combinatorial Optimization by Stochastic
     Evolution," IEEE Transactions on Computer-Aided Design, vol. 10(4), 1981.
"""
import numpy as np
from . import objective_functions


__author__ = "Damar Wicaksono"


def init_threshold(dm: np.ndarray):
    """Calculate the initial threshold as recommended in the article

    :param dm: the initial design matrix
    :return: the initial threshold
    """
    pass


def num_candidate(n: int) -> int:
    """Calculate the number of candidates from perturbing the current design

    :param n: the number of elements to be permuted
    :return: the number of candidates from perturbing the current design
        column-wise
    """
    pass


def max_inner(k: int) -> int:
    """Calculate the maximum number of inner iterations

    :param k: the number of design dimension
    :return: the maximum number of inner iterations/loop
    """
    pass


def perturb(dm, num_dimension, num_candidate, obj_function):
    """Create new configuration of a design matrix according to ESE algorithm

    According to the algorithm, a distinct `num_candidate` designs have to be
    generated from the current design by carrying out a column-wise perturbation
    on a given colum, `num_dimension`. The best design according to the select
    `obj_function` will be selected as the "perturbed" design

    :param dm: the current design matrix
    :param num_dimension: the column of design matrix to be perturbed
    :param num_candidate: the number of distinct candidates to be generated
    :param obj_function: the select objective function
    :return: the perturbed state of the current design
    """
    pass


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
        if 0 calculate from the recommended value
    :param m: the maximum number of inner iterations, if 0 calculate from the
        recommended value
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
    pass
