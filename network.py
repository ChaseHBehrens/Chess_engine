import tensorflow as tf
import random

# Define the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(64, input_shape=(64,), activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

for i in range(5):
    #set data
    def generate_random_list():
      lst = [0] * 64
      index = random.randint(0, 63)
      lst[index] = 1
      return lst
    x_train = [generate_random_list() for i in range(1000)]
    y_train = [[x_train[j].index(1)] for j in range(1000)]

    # Train the model
    model.fit(x_train, y_train, epochs=1)

    for i in range(10):
        random_list = generate_random_list()
        print(random_list.index(1))
        prediction = model.predict([random_list])[0][0]
        print(prediction)

