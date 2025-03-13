import numpy as np
from sklearn import datasets
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, neuron_network):
        self.bias = []
        # Веса необходимы как передача информации от одного нейрона к другим неронам лежащим на следующем уровне сети
        self.weights = []
        # Все нейроны которые будут созданы
        self.neuron = []
        self.neuron_network = neuron_network
        for index in range(1, len(neuron_network)):
            self.weights.append(np.random.rand(neuron_network[index-1], neuron_network[index]))
            self.bias.append(np.random.rand(1, neuron_network[index]))
        # Инициализация весов и смещений между слоями
        self.weights_input_hidden1 = np.random.rand(neuron_network[0], neuron_network[1])
        self.bias_hidden1 = np.random.rand(1, neuron_network[1])

        # self.weights_hidden1_hidden2 = np.random.rand(neuron_network[1], neuron_network[2])
        self.bias_hidden2 = np.random.rand(1, neuron_network[2])

        # self.weights_hidden2_output = np.random.rand(neuron_network[2], neuron_network[-1])
        self.bias_output = np.random.rand(1, neuron_network[-1])

    def feedforward(self, X):
        # Прямое распространение
        self.layer_input = []
        self.layer_output = []
        for index in range(len(self.weights)):
            if index == 0:
                sum_element = np.dot(X, self.weights[index]) + self.bias[index]
                self.layer_input.append(sum_element)
                self.layer_output.append(sigmoid(sum_element))
            else :
                sum_element = np.dot(self.layer_output[-1], self.weights[index]) + self.bias[index]
                self.layer_output.append(sigmoid(sum_element))
        self.final_output = self.layer_output[-1]
        return self.final_output

    def backpropagate(self, X, y, learning_rate):
        # Обратное распространение
        layer_delta = []
        
        output_error = y - self.layer_output[-1]
        hidden_layer_error = []
        for index in range(len(self.layer_output), 0, -1):
            if index == len(self.layer_output):
                layer_delta.insert(0, output_error * sigmoid_derivative(self.layer_output[index-1]))
                hidden_layer_error.insert(0, layer_delta[0].dot(self.weights[index-1].T))
            else:
                layer_delta.insert(0, hidden_layer_error[0] * sigmoid_derivative(self.layer_output[index-1]))
                hidden_layer_error.insert(0, layer_delta[0].dot(self.weights[index-1].T))

        for index in range(len(self.weights)):
            if index == 0:
                self.weights[index]+= X.T.dot(layer_delta[index]) * learning_rate
                self.bias[index] += np.sum(layer_delta[index], axis=0, keepdims=True) * learning_rate
            else:
                self.weights[index] += self.layer_output[index - 1].T.dot(layer_delta[index]) * learning_rate
                self.bias[index] += np.sum(layer_delta[index], axis=0, keepdims=True) * learning_rate


    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            self.feedforward(X)
            self.backpropagate(X, y, learning_rate)

# Данные для задачи XOR
X = np.array([
    [-2, -1],  # Алиса
    [25, 6],   # Боб
    [17, 4],   # Чарли
    [-15, -6], # Диана
])

y = np.array([[1, 0],  # 0
              [0, 1],  # 1
              [0, 1],  # 1
              [1, 0]]) # 0

# Инициализация и обучение
# iris = datasets.load_iris()
# dataset = [(iris.data[i][None, ...], iris.target[i]) for i in range(len(iris.target))]
# print("dataset", dataset)
# exit()
nn = NeuralNetwork([2,6,6,2])
nn.train(X, y, epochs=10000, learning_rate=0.1)




emily = np.array([-7, -3]) # 128 фунтов (52.35 кг), 63 дюйма (160 см)
frank = np.array([20, 2])  # 155 pounds (63.4 кг), 68 inches (173 см)
print("Эмили:", nn.feedforward(emily)) # 0.951 - Ж
print("Фрэнк:", nn.feedforward(frank)) # 0.039 - М