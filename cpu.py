import time
import platform

# Define a function to be benchmarked
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

# Start the timer
start_time = time.time()

# Call the function to be benchmarked
result = fib(45)

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time


if platform.system() == "Linux":
    import psutil
    temps = psutil.sensors_temperatures()
    cpu_temp = temps["coretemp"][0].current
    print(f"CPU Temp: {cpu_temp}")

print(f"Result: {result}")
print(f"Elapsed time: {elapsed_time}")
