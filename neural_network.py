import math

class Perceptron(object):
    """
    Base class of a neuron using the perceptron algorithm.

    Arguments:
    size_inputs -- Integer : the size of the input of the neuron
    """
    def __init__(self, size_inputs):
        super(Perceptron, self).__init__()
        self.size_inputs = size_inputs
        self.weights = tuple(0 for _ in xrange(self.size_inputs))

    def apply_weight(self, inputs):
        """
        Apply weight of the neuron of the input *inputs*.

        Arguments:
        inputs -- [Real] : Input

        Returns:
        [Real] : The ponderated vector input

        Raises:
        AssertionError : if the length of the input is different of the length
        of
        the weights
        """
        assert len(inputs) == self.size_inputs
        W = self.weights
        return [x * w for w, x in zip(inputs, W)]

    @classmethod
    def aggregate(_, weighted_input):
        """
        Aggragate function of a learning machine with neural network.
        Sum the vector *weighted_input* and return the result.

        Arguments:
        weighted_input -- [Real] : Vector to aggregate

        Returns:
        Real : Sum of the vector *weighted_input*
        """
        return sum(weighted_input)

    @classmethod
    def threshold(_, aggregated_input):
        """
        Threashold function of a learning machine with neural network.
        Put *aggregated_input* into a sigmoid function and return the result.

        Arguments:
        aggregated_input -- Real : Input of the threashold function.

        Returns:
        Real [0 ; 1] : An real between 0 and 1 corresponding to the result of a
        sigmoid function.
        """
        param = 1.0
        return 1 if aggregated_input >= 0 else 0
        return 1.0 / (1.0 + math.exp(- param * aggregated_input))

    def weights_fix(self, X, true_result, result):
        """
        Learning rule fixing the current weight by considering the distance
        between the expected result *true_result* and the obtained result
        *result* with the input *inputs*.

        Arguments:
        X           -- [Real] : Input used with the current experience
        true_result -- Real : Expected result of the experience
        result      -- Real : Obtained result

        Raises:
        AssertionError : if the length of the input is different of the length
        of the weights
        """
        assert len(X) == self.size_inputs
        learning_step = 0.1
        dr = true_result - result
        W = self.weights
        self.weights = tuple(w + learning_step * dr * x for w, x in zip(W, X))

    def eval(self, X):
        """
        Apply the logic neural network system on the input *X*.

        Arguments:
        X -- [Real] : Input

        Returns:
        Real : the solution calculated by the neuron.
        """
        return Perceptron.threshold(Perceptron.aggregate(self.apply_weight(X)))

    def learn(self, X, result):
        """
        Eval the input *X* with the neuron and compare it with the expected
        result *result* to learn the neuron.

        Arguments:
        X      -- [Real] : Input
        result -- Real : Expected result

        Returns:
        The current evaluation of the input by the neuron.
        """
        r = self.eval(X)
        self.weights_fix(X, result, r)
        return r

if __name__ == '__main__':
    inputs = [(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    results = [0, 0, 0, 1]
    neuron = Perceptron(3)
    error = True

    while error:
        error = False
        for X, R in zip(inputs, results):
            res = neuron.learn(X, R)
            print X, R, res
            error |= res != R
