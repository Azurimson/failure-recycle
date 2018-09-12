from keras.models import Sequential
from keras.layers import Dense
import numpy

dataset = numpy.loadtxt("dataset.csv", delimiter=" ")
X_train = dataset[:, :-1]
Y_train = dataset[:, -1:]

model = Sequential()
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, Y_train, validation_split=0.3, epochs=20, batch_size=100, verbose=1)

loss, accuracy = model.evaluate(X_train, Y_train)
print(loss, accuracy)

print(X_train[-1:, ])
print(Y_train[-1:, ])
pred = model.predict(X_train[-1:, ])
print(pred)

model.save('minemodel.h5')