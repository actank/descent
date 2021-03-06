"""
Test suite for matrix approximation
"""
import numpy as np
from descent import algorithms
from descent.proxops import nucnorm


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

    # helper function to test relative error of given parameters
    def test_error(Xhat):
        test_err = np.linalg.norm(Xhat - Xtrue, 'fro')
        naive_err = np.linalg.norm(Xobs - Xtrue, 'fro')
        err_ratio = test_err / naive_err
        assert err_ratio <= 0.5

    # Proximal gradient descent and Accelerated proximal gradient descent
    for algorithm in ['sgd', 'nag']:

        # objective
        def f_df(X):
            grad = X - Xtrue
            obj = 0.5 * np.linalg.norm(grad.ravel()) ** 2
            return obj, grad

        # optimizer
        opt = getattr(algorithms, algorithm)(lr=5e-3)
        opt.operators.append(nucnorm(0.2))

        # run it
        res = opt.minimize(f_df, Xobs, maxiter=5000, display=None)

        # test
        test_error(res.x)
