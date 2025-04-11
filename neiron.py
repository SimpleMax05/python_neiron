import numpy as np

class Neuron:
    # weight входные веса для нейрона
    # bias смещение для некрона
    def __init__(self, weight, bias: float, weight_out = []):
        self.total = 0
        # Ответ который получается из нейрона после прохождения функции активации
        self.total_in_sigmoid = 0
        self.weight = weight
        self.bias = bias
        self.weight_out = weight_out
    # Функция переключения 1/0
    def sigmoid(sels, x):
        return 1 / (1 + np.exp(-x))
    # Производная от сигмойдной функции
    def deriv_sigmoid(self):
        # Cигмойд будет высчитан до необходимости в производной
        fx = self.total_in_sigmoid
        return fx * (1 - fx)
    # weight для входа нейрона
    # inputs это слой который лежит перед нейроном
    # weight должен соотвествовать связанному с ним input
    def feedforward(self, inputs):
        total = np.dot(self.weight, inputs) + self.bias
        self.total = total
        self.total_in_sigmoid = self.sigmoid(total)
        return self.total_in_sigmoid