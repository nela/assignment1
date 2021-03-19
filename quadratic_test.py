import numpy as np
import cvxopt

G = np.array([
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [-1, 0, 0, 0, 0],
    [0, -1, 0, 0, 0],
    [0, 0, -1, 0, 0],
    [0, 0, 0, -1, 0],
    [0, 0, 0, 0, -1],
    ])

h = np.array([3, 3, 3, 3, 3, 0, 0, 0, 0, 0])

P = np.array([
    [.9, .1, .2, .15, .11],
    [.9, .1, .2, .15, .11],
    [.9, .1, .2, .15, .11],
    [.9, .1, .2, .15, .11],
    [.9, .1, .2, .15, .11]])

np.random.seed(4)
pr = np.random.random(4)
pr = [1, 1, 1, 1, 1]
q = np.append(pr, pr)
q=np.array(pr)
A = np.array([
    [1, 1, 1, 1, 1]
    ])


b = np.array([9])

def cvxopt_solve_qp(P, q, G=None, h=None, A=None, b=None):
    P = .5 * (P + P.T)  # make sure P is symmetric
    args = [cvxopt.matrix(P), cvxopt.matrix(q)]
    if G is not None:
        args.extend([cvxopt.matrix(G), cvxopt.matrix(h)])
        if A is not None:
            args.extend([cvxopt.matrix(A), cvxopt.matrix(b)])
    return cvxopt.solvers.qp(*args)

print(q)
sol = cvxopt_solve_qp(P, q.astype('float'), G.astype('float'), h.astype('float'), A.astype('float'), b.astype('float'))

print(sol)
print(np.round_(np.array(sol['x']).reshape(P.shape[1],), decimals=2))
# print(np.array(sol['y']))
# print(np.array(sol['s']))
# print(np.array(sol['z']))
