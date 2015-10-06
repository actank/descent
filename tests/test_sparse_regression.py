"""
Test suite for sparse regression

"""

import numpy as np
from descent import ADMM


def generate_sparse_system(n=100, m=50, p=0.1, eta=0.05, seed=1234):
    """
    Generate a sparse, noisy system

    """
    print("Generating data for sparse regression")
    global x_true, x_obs, A

    # define the seed
    np.random.seed(seed)

    # the true sparse signal
    x_true = 10 * np.random.randn(n) * (np.random.rand(n) < p)

    # the noisy, observed signal
    A = np.random.randn(m, n)
    y = A.dot(x_true)

    return A, y, x_true


def test_sparse_regression():
    """
    Test sparse regression

    """

    A, y, x_true = generate_sparse_system()

    # least squares solution
    xls = np.linalg.lstsq(A, y)[0]

    # proximal algorithm for sparse regression
    opt = ADMM(xls)
    opt.add('linsys', A=A, b=y)
    opt.add('sparse', 1.)
    opt.display = None
    opt.storage = None
    opt.run(maxiter=100)
    xhat = opt.theta

    test_err = np.linalg.norm(xhat - x_true, 2)
    naive_err = np.linalg.norm(xls - x_true, 2)
    err_ratio = test_err / naive_err
    print("The error ratio is: %5.4f" % err_ratio)

    assert err_ratio <= 0.01