import tensorflow as tf
import time

# Adjust for the size of the matrices. The higher value results in longer execution time.
matrix_n = 20000

# Adjust the following value to match your CPU's number of cores.
tf.config.threading.set_inter_op_parallelism_threads(16)

# Check if a GPU is available
if tf.config.list_physical_devices('GPU'):
    print("Using GPU")
else:
    print("No GPU found, using CPU")

# Define the matrices to be multiplied
matrix1 = tf.random.normal([matrix_n, matrix_n])
matrix2 = tf.random.normal([matrix_n, matrix_n])

# Start the timer
start_time = time.time()

# Perform the matrix multiplication on the GPU
product = tf.matmul(matrix1, matrix2)

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time)