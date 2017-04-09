# -*- coding: utf-8 -*-
"""indices_1st.py: Module to calculate the 1st-order Sobol' indices
"""
import numpy as np

__author__ = "Damar Wicaksono"


def evaluate(y_dict: dict, estimator="sobol-saltelli") -> dict:
    """Calculate the 1st-order Sobol' sensitivity indices and create a dict

    This is a driver function to call several choices of 1st-order index
    estimators. The input is a dictionary of output vectors.

    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: (str) which estimator to use
    :return: a dictionary of all the indices
    """
    pass


def bootstrap(y_dict: dict, estimator="sobol-saltelli",
              n_samples=10000, seed=20151418) -> dict:
    """Generate bootstrap samples and calculate the confidence intervals

    Two kind of confidence intervals are provided, both are 95% confidence
    intervals:
        1. Standard error (normality assumption, +/-1.96*SE gives the coverage)
        2. Percentile confidence intervals, by using order statistics

    **References:**

    (1) G.E.B Archer, A. Saltelli, and I.M. Sobol', "Sensitivity measures,
        ANOVA-like techniques and the use of bootstrap," Journal of Statistical
        Computation and Simulation," vol. 58, pp. 99-120, 1997

    :param y_dict: a dictionary of numpy array of model outputs
    :param estimator: (str)
    :param n_samples:
    :param seed:
    """
    pass


def janon(fb: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the 1st-order Sobol' indices using the Janon estimator

    This function is an implementation of Janon's second estimator given by
    Equation (6), pp. 4, in [1].

    **References:**

    (1) A. Janon, et al., "Asymptotic normality and efficiency of two Sobol'
        index estimators," ESAIM: Probability and Statistics, EDP Sciences,
        2003

    :param fb: numpy array of model output with matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :return: (float) the 1st-order index for parameter-i
    """
    pass


def sobol_saltelli(fa: np.ndarray, fb: np.ndarray, fab_i: np.ndarray) -> float:
    """Calculate the 1st-order index for parameter-i using Sobol'-Saltelli

    The implementation below is based on the Sobol'-Saltelli Design given in
    Table 2 of [1] (equation (b)). This estimator is still the same as the one
    proposed in the older publication, given in Table 1 of [2].

    **References:**

    (1) A. Saltelli, et al., "Variance based sensitivity analysis of model
        output. Design and estimator for the total sensitivity index,"
        Computer Physics Communications, 181, pp. 259-270, 2010
    (2) A. Saltelli, "Making best use of model evaluations to compute
        sensitivity indices," Computer Physics Communications, 145, pp. 280-297,
        2002

    :param fa: numpy array of model output with matrix A
    :param fb: numpy array of model output with matrix B
    :param fab_i: numpy array of model output with matrix AB_i
    :return: the 1st-order index for parameter-i
    """
    pass
