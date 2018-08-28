from keras.models import Sequential
from keras.layers import Dense
import numpy

def create_model():
    dataset = numpy.loadtxt("dataset.csv", delimiter=" ")
    X_train = dataset[:, :-1]
    Y_train = dataset[:, -1:]

    model = Sequential()
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['accuracy'])

    model.fit(X_train, Y_train, validation_split = 0.1, epochs=10, batch_size=10, verbose=1)

    return model

def predict_next(model, board):
    X_test = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 10:
                X_test_cache = []
                for x in board:
                    for y in x:
                        X_test_cache.append(y)
                X_test_cache.append(i)
                X_test_cache.append(j)
                X_test.append(X_test_cache)
    X_test = numpy.array(X_test, dtype = numpy.int32)
    predictions = model.predict(X_test)
    m = max(predictions[:, -1:])
##    predictions = predictions.tolist()
    for i in range(len(predictions)):
        if m in predictions[i]:
            break
    res = X_test[i, -2:]
    
    write_file(X_test, predictions, res)
    
    return res[0], res[1]

def write_file(X_test, predictions, res):
    file = open('cache', 'a')
    X_test = X_test.tolist()
    predictions = predictions.tolist()
    for i in X_test:
        for j in i:
            file.write(str(j) + ' ')
        file.write('\n')
    file.write('\n')
    for i in predictions:
        for j in i:
            file.write(str(j) + ' ')
        file.write('\n')
    file.write('\n')
    file.write(str(res[0]))
    file.write('\n')
    file.write(str(res[1]))
    file.write('\n')
    file.close()
