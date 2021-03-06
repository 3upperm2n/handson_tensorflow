import tensorflow as tf
import numpy as np
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
m,n=housing.data.shape                          # m : number of records, n : features
print("housing data : ({}, {})".format(m, n))

housing_data_plus_bias = np.c_[np.ones((m,1)), housing.data]
print housing_data_plus_bias.shape

n_epochs = 1000
learning_rate = 0.01 

X = tf.constant(housing_data_plus_bias, dtype=tf.float32, name="X")

y = tf.constant(housing.target.reshape(-1, 1), dtype=tf.float32, name="y")

theta = tf.Variable(tf.random_uniform([n + 1, 1], -1.0, 1.0), name="theta")

y_pred = tf.matmul(X, theta, name="predictions")

error = y_pred - y

mse = tf.reduce_mean(tf.square(error), name="mse")

#
#opt 1
#
## partial derivatives fo the cost function
gradients = 2/m * tf.matmul(tf.transpose(X), error)   # default: manually  (work!)
training_op = tf.assign(theta, theta - learning_rate * gradients)

##
##opt 2
##
#gradients =  tf.gradients(mse, [theta])[0]  # audodiff: this did not work! ???
#training_op = tf.assign(theta, theta - learning_rate * gradients)


##
##opt 3
##
#optimizer = tf.train.GradientDescentOptimizer(learning_rate = learning_rate)
#training_op = optimizer.minimize(mse)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for epoch in range(n_epochs):
        if epoch % 100 == 0:
            print("Epoch", epoch, "MSE = ", mse.eval())
        sess.run(training_op)

    best_theta = theta.eval()

print best_theta

