import numpy as np
import json
from tqdm import tqdm
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

def to_full(y, num_classes):
    y_full = np.zeros((1, num_classes))
    y_full[0, int(y)] = 1  # Используйте целочисленный индекс
    return y_full

def n_array_to_array(n_array):
    return n_array.flatten().reshape(1, -1)  # Плоский массив в форму (1, -1)

arr_los = []

def load(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    net = NeuralNetwork(data["neuron_network"])
    net.weights = [np.array(w) for w in data["weights"]]
    net.bias = [np.array(b) for b in data["biases"]]
    return net
class NeuralNetwork:
    def __init__(self, neuron_network):
        self.bias = []
        self.weights = []
        self.neuron_network = neuron_network
        for index in range(1, len(neuron_network)):
            self.weights.append(np.random.randn(neuron_network[index-1], neuron_network[index]) * 0.01)  # Нормальная инициализация
            self.bias.append(np.random.randn(1, neuron_network[index]) * 0.01)
    def save(self, filename):
        data = {"neuron_network": self.neuron_network,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.bias]}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()
    # Получить ответ на вход передаётся массив из входных элементов
    def feedforward(self, X):
        self.layer_input = []
        self.layer_output = []
        for index in range(len(self.weights)):
            if index == 0:
                sum_element = np.dot(X, self.weights[index]) + self.bias[index]
                self.layer_output.append(sigmoid(sum_element))
            else:
                sum_element = np.dot(self.layer_output[index-1], self.weights[index]) + self.bias[index]
                self.layer_output.append(sigmoid(sum_element))
        self.final_output = self.layer_output[-1]
        return self.final_output

    def backpropagate(self, X, y, learning_rate):
        output_error = y - self.layer_output[-1]

        # Упрощение логирования потерь
        loss = np.sum(np.abs(output_error))
        arr_los.append(loss)

        layer_delta = [output_error * sigmoid_derivative(self.layer_output[-1])]

        for index in range(len(self.layer_output)-1, 0, -1):
            hidden_layer_error = layer_delta[0].dot(self.weights[index].T)
            layer_delta.insert(0, hidden_layer_error * sigmoid_derivative(self.layer_output[index - 1]))

        for index in range(len(self.weights)):
            if index == 0:
                self.weights[index] += X.T.dot(layer_delta[index]) * learning_rate
                self.bias[index] += np.sum(layer_delta[index], axis=0, keepdims=True) * learning_rate
            else:
                self.weights[index] += self.layer_output[index - 1].T.dot(layer_delta[index]) * learning_rate
                self.bias[index] += np.sum(layer_delta[index], axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in tqdm(range(epochs), "epoch"):
            for i in range(len(X)):
                y_array = to_full(y[i], self.neuron_network[-1])
                x_array = n_array_to_array(X[i])
                self.feedforward(x_array)
                self.backpropagate(x_array, y_array, learning_rate)

def max_index(array):
    max_index = 0
    max = array[0][0]
    for item in range(len(array[0])):
        if max < array[0][item]:
            max_index = item
            max = array[0][item]
    return max_index
# Инициализация и обучение