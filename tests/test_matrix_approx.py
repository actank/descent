"""
Test suite for matrix approximation

"""

import numpy as np
from descent import ADMM


def generate_lowrank_matrix(n=10, m=20, k=3, eta=0.05, seed=1234):
    """
    Generate an n-by-m noisy low-rank matrix

    """
    print("Generating data for low rank matrix approximation")
    global Xtrue, Xobs

    # define the seed
    np.random.seed(seed)

    # the true low-rank matrix
    Xtrue = np.sin(np.linspace(0, 2 * np.pi, n)).reshape(-1, 1).dot(
        np.cos(np.linspace(0, 2 * np.pi, m)).reshape(1, -1))

    # the noisy, observed matrix
    Xobs = Xtrue + eta * np.random.randn(n, m)

    return Xobs, Xtrue


def test_lowrank_matrix_approx():
    """
    Test low rank matrix approximation

    """

    Xobs, Xtrue = generate_lowrank_matrix()

    # proximal algorithm for low rank matrix approximation
    opt = ADMM(Xobs)
    opt.add('squared_error', Xobs)
    opt.add('nucnorm', 0.2)
    opt.display = None
    opt.storage = None
    opt.run(maxiter=100)
    Xhat = opt.theta

    test_err = np.linalg.norm(Xhat - Xtrue, 'fro')
    naive_err = np.linalg.norm(Xobs - Xtrue, 'fro')
    err_ratio = test_err / naive_err
    print("The error ratio is: %5.4f" % err_ratio)

    assert err_ratio <= 0.5