import numpy as np
from neiron import Neuron
import statistics



def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def deriv_sigmoid(x):
  # Производная сигмоиды: f'(x) = f(x) * (1 - f(x))
  fx = sigmoid(x)
  return fx * (1 - fx)

def mse_loss(y_true, y_pred):
  # y_true и y_pred - массивы numpy одинаковой длины.
  return ((y_true - y_pred) ** 2).mean()


    
class OurNeuralNetwork:
    
    '''
    Все нейроны имеют одинаковые веса и пороги:
        - w = [0, 1]
        - b = 0
        [10, 7, 6, 5, 1] 
    '''
    def create_neuron(self, neuron_network):
        self.neuron = []
        count = len(neuron_network)
        # Создаём нейроны
        for itemI in range(1, count):
            neuron_layer = []
            # Проблема в том что мы должны передать ему значения веса 
            for itemJ in range(neuron_network[itemI]):
                neuron_weight = self.weights[itemI-1][itemJ]
                bias_neuron = self.bias[itemI-1][0][itemJ]
                neuron_layer.append(Neuron(neuron_weight, bias_neuron))
            self.neuron.append(neuron_layer)
    def __init__(self, neuron_network):
        # Пороги необходимы для вычислений всех элментов кроме входных параметров
        self.bias = []
        # Веса необходимы как передача информации от одного нейрона к другим неронам лежащим на следующем уровне сети
        self.weights = []
        # Все нейроны которые будут созданы
        self.neuron = []
        for index in range(1, len(neuron_network)):
            self.weights.append(np.random.rand(neuron_network[index-1], neuron_network[index]))
            self.bias.append(np.random.rand(1, neuron_network[index]))
        self.create_neuron(neuron_network)
        # Метод подсчитывающий ответ. Проход по всем нейронам слой за слоем и получение ответа
        
    
    # Получение ответа нейросети 
    # где X это входная последовательность
    def feedforward(self, x):
        inputs_in = x
        input_out = []
        for item_layer in range(len(self.neuron)):
            input_out = []
            for item_neuron in range(len(self.neuron[item_layer])):
                neuron_l_i: Neuron = self.neuron[item_layer][item_neuron]
                element_out = neuron_l_i.feedforward(inputs_in)
                input_out.append(element_out)
            inputs_in = input_out
        return input_out
    def train(self, data, all_y_trues):
        learn_rate = 0.01
        epochs = 1000 # сколько раз пройти по всему набору данных 
        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):
                y_pred = self.feedforward(x)
                total = []
                neuron_out = []
                neuron_deriv = []
                for indexI in range(len(self.neuron)):
                    total.append([])
                    neuron_out.append([])
                    neuron_deriv.append([])
                    for indexJ in range((len(self.neuron[indexI]))):
                        total[indexI].append(self.neuron[indexI][indexJ].total)
                        neuron_out[indexI].append(self.neuron[indexI][indexJ].total_in_sigmoid)
                        neuron_deriv[indexI].append(self.neuron[indexI][indexJ].deriv_sigmoid())
                print("total", total)
                print("neuron_out", neuron_out)
                print("neuron_deriv", neuron_deriv)
                exit()
                # --- Считаем частные производные.
                # --- Имена: d_L_d_w1 = "частная производная L по w1"
                # Получаем вектор ошибки на последнем слое
                d_L_d_ypred = []
                for index in range(len(y_true)):
                    d_L_d_ypred.append(y_pred[index] - y_true[index])
                dE_dW_all = []
                dE_db_all = []
                # Backward
                # Получаем полный вектор правильного ответа
                # y_full = to_full(y, OUT_DIM)
                # Получаем ошибку на выходном слое
                # dE_dt2 = d_L_d_ypred # z - y_full
                # print("d_L_d_ypred", d_L_d_ypred)
                # # Тут получаем смещения для весов между скрытым и выходным слоем
                # dE_dW2 = h[0].T @ dE_dt2
                # dE_db2 = dE_dt2
                # # Высчитываем ошибку для предыдущего слоя
                # dE_dh1 = dE_dt2 @ w_all[1].T
                # dE_dt1 = dE_dh1 * relu_deriv(t[0])
                # dE_dW1 = x.T @ dE_dt1
                # dE_db1 = dE_dt1
                # dE_dW_all.insert(0, dE_dW2)
                # dE_db_all.insert(0, dE_db2)
                # dE_dW_all.insert(0, dE_dW1)
                # dE_db_all.insert(0, dE_db1)
                # Update Изменяем веса и смещения на основании обратного прохода
                for w_index in range(len(w_all)):
                    w_all[w_index] = w_all[w_index] - learn_rate * dE_dW_all[w_index]
                for b_index in range(len(b_all)):
                    b_all[b_index] = b_all[b_index] - learn_rate * dE_db_all[b_index]
            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.feedforward, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f" % (epoch, loss))


    
if __name__ == "__main__":
    data = np.array([
    [-2, -1],  # Алиса
    [25, 6],   # Боб
    [17, 4],   # Чарли
    [-15, -6], # Диана
    ])
    all_y_trues = np.array([
    [1, 0], # Алиса
    [0, 1], # Боб
    [0, 1], # Чарли
    [1, 0], # Диана
    ])
    network = OurNeuralNetwork([2,2,2])
    network.train(data, all_y_trues)
    # Делаем пару предсказаний
    emily = np.array([-7, -3]) # 128 фунтов (52.35 кг), 63 дюйма (160 см)
    frank = np.array([20, 2])  # 155 pounds (63.4 кг), 68 inches (173 см)
    print("Эмили:", network.feedforward(emily)) # 0.951 - Ж
    print("Фрэнк:", network.feedforward(frank)) # 0.039 - М
    