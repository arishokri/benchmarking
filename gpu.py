import tensorflow as tf
import time

# Define the matrices to be multiplied
matrix1 = tf.random.normal([10000, 10000])
matrix2 = tf.random.normal([10000, 10000])

# Start the timer
start_time = time.time()

# Perform the matrix multiplication on the GPU
product = tf.matmul(matrix1, matrix2)

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time)