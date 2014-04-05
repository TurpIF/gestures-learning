import math

def aggregate_funct(X):
    """
    Aggragate function of a learning machine with neural network.
    Sum the vector *X* and return the result.

    Arguments:
    X -- [Real] : Vector to aggregate

    Returns:
    Real : Sum of the vector *X*
    """
    return sum(X)

def threshold_funct(Z):
    """
    Threashold function of a learning machine with neural network.
    Put *Z* into a sigmoid function and return the result.

    Arguments:
    Z -- Real : Input of the threashold function.

    Returns:
    Real [0 ; 1] : An real between 0 and 1 corresponding to the result of a sigmoid function.
    """
    param = 1.0
    return 1 if Z >= 0 else 0
    return 1.0 / (1.0 + math.exp(- param * Z))

def weight_fix(weight, true_result, result, input):
    """
    Learning rule fixing the current weight *weight* by considering the
    distance between the expected result *true_result* and the obtained result
    *result* with the input *input*.

    Arguments:
    weight      -- Real : Current weight
    true_result -- Real : Expected result of the experience
    result      -- Real : Obtained result
    input       -- Real : Input used with the current experience

    Returns:
    Real : The new weight calculated to reduce the error.
    """
    learning_step = 0.1
    return weight + learning_step * (true_result - result) * input

def apply_weight(X, W):
    """
    Apply weight *W* of the neurone of the input *X*.

    Arguments:
    X -- [Real] : Input
    W -- [Real] : Weight of the neurone

    Returns:
    [Real] : The ponderated vector input

    Raises:
    AssertionError : if the length of the input is different of the length of
    the weights
    """
    assert len(X) == len(W)
    return [x * w for w, x in zip(X, W)]

def apply(X, W, f_agg, f_threshold):
    """
    Apply the logic neural network system on the input *X* with the weights
    *W*, the aggregate function *f_agg* and the threshold function
    *f_threshold*.

    Arguments:
    X -- [Real] : Input

    Returns:
    Real : the solution calculated by the neurone.
    """
    return f_threshold(f_agg(apply_weight(X, W)))

if __name__ == '__main__':
    inputs = [(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    results = [0, 0, 0, 1]
    weights = (0, 0, 0)
    error = True

    while error:
        error = False
        for X, R in zip(inputs, results):
            res = apply(X, weights, aggregate_funct, threshold_funct)
            print X, R, weights, res
            weights = tuple(weight_fix(w, R, res, x) for w, x in zip(weights, X))
            error |= res != R
