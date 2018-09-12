from keras.models import Sequential
from keras.layers import Dense
import numpy

def predict_next(model, plist):
    X_test = []
    X_test.append(plist)
    X_test = numpy.array(X_test, dtype=numpy.int32)
    predictions = model.predict(X_test)
    return predictions

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
