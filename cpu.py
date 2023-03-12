import time

# Define a function to be benchmarked
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

# Start the timer
start_time = time.time()

# Call the function to be benchmarked
result = fib(40)

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time

print("Result:", result)
print("Elapsed time:", elapsed_time)
