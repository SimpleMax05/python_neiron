from network import NeuralNetwork, max_index, load
from keras.datasets import mnist
import os

if __name__ == "__main__":
    (train_X, train_y), (test_X, test_y) = mnist.load_data()

    # Предобработка данных
    train_X = train_X.reshape(-1, 28 * 28) / 255.0
    test_X = test_X.reshape(-1, 28 * 28) / 255.0


    if os.path.isfile("neuron_networ.json"):
        nn = load("neuron_networ.json")
    else:
        nn = NeuralNetwork([784, 16, 16, 10])
        nn.train(train_X, train_y, epochs=40, learning_rate=0.04)
        nn.save("neuron_networ.json")
    x_array = test_X
    print("x_array[0]", x_array[0])
    answer = nn.feedforward(x_array[0])
    ans = max_index(answer)
    print("answer f'{answer:.10f}'", answer, ans, test_y[0])

    answer = nn.feedforward(x_array[1])
    ans = max_index(answer)
    print("answer", answer, ans, test_y[1])

    answer = nn.feedforward(x_array[2])
    ans = max_index(answer)
    print("answer", answer, ans, test_y[2])

    answer = nn.feedforward(x_array[3])
    ans = max_index(answer)
    print("answer", answer, ans, test_y[3])