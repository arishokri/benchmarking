import torch
import time
from datetime import datetime
import os
import platform
from typing import Tuple
import re


def stress_gpu_with_matrix_operations(matrix_size, iterations, torch_device) -> float:
    """
    Performs matrix multiplication on the GPU for a specified duration.

    Parameters:
        duration_seconds (float): The time (in seconds) to run the matrix operations.

    Returns:
        int: The number of matrix multiplications performed.
    """
    size = matrix_size  # Adjust size as needed to stress the GPU
    # Track time and number of multiplications
    start_time = time.time()
    iteration = 0
    while iteration < iterations:
        # Create large matrices for multiplication on GPU (CUDA)
        matrix_a = torch.rand(size, size, device=torch_device)
        matrix_b = torch.rand(size, size, device=torch_device)
        # Run matrix multiplications until the number of iterations is reached.
        torch.matmul(matrix_a, matrix_b)  # Matrix multiplication using PyTorch
        # torch.cuda.synchronize()  # Ensure GPU operations complete
        iteration += 1
    runtime = time.time() - start_time
    return runtime


def get_cpu_temp(system="Linux") -> int:
    """
    This will only work on Linux
    On Linux, this reads temperatures from system sensors.
    psutil.sensors_temperatures() provides info if available.
    """
    if system == "Linux":
        temps = psutil.sensors_temperatures()
    else:
        temps = None
    if "coretemp" in temps:  # Gets a sample of CPU temp readings.
        n_sensors = len(temps["coretemp"])
        package_temp = temps["coretemp"][0].current
        core_1 = temps["coretemp"][n_sensors // 2].current
        core_2 = temps["coretemp"][n_sensors - 1].current
    else:
        package_temp = core_1 = core_2 = None
    return package_temp, core_1, core_2


def get_gpu_temp(system="Linux") -> Tuple[int, int]:
    # Only works on Linux platform.
    if system == "Linux":
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assumes the first GPU
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        clock = utilization.gpu
        memory = utilization.memory
    elif system == "Darwin":
        temp = clock = memory = "Running on Darwin System"
    else:
        temp = clock = memory = "Running on Unknown OperatingSystem"
    return temp, clock, memory


def log_performance(
    logfile, test_duration=60, matrix_size=1024, iterations=10, system="Linux"
) -> None:
    if system == "Linux":
        torch_device = "cuda"
    elif system == "Darwin":
        torch_device = "mps"
    else:
        raise SystemError("Unknown/Unsupported Operating System")

    with open(logfile, "a") as f:
        header = (
            "Timestamp, GPU Temp (°C), GPU Clock (%), GPU Memory (%), "
            "CPU Package (°C), CPU Core 1 (°C), CPU Core 2 (°C), Matrix Time (s)\n"
        )
        print(header + "\n")
        f.write(header)
        start_time = time.time()
        # Perform matrix operation and log its duration
        while time.time() - start_time < test_duration:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            gpu_temp, gpu_clock, gpu_memory = get_gpu_temp(system=system)
            cpu_package, cpu_core_1, cpu_core_2 = get_cpu_temp(system=system)
            matrix_time = stress_gpu_with_matrix_operations(
                matrix_size=matrix_size,
                iterations=iterations,
                torch_device=torch_device,
            )
            # Get CPU and GPU metrics on systems that support them.
            # Log metrics
            log_entry = (
                f"{timestamp}, {gpu_temp}, {gpu_clock}, {gpu_memory}, "
                f"{cpu_package}, {cpu_core_1}, {cpu_core_2}, {matrix_time:.4f}\n"
            )

            print(log_entry.strip())
            f.write(log_entry)
            # Wait for a number of seconds.
            time.sleep(2)


if __name__ == "__main__":
    duration = 300  # Sets test duration in seconds.
    matrix_size = 15000
    iterations = 100
    system = platform.system()
    if system == "Linux":
        import psutil
        import pynvml

        torch_device = "cuda"
    elif platform.system() == "Darwin":
        torch_device = "mps"

    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/pytorch_{duration}s.csv"
    log_performance(
        logfile=log_file,
        test_duration=duration,
        matrix_size=matrix_size,
        iterations=iterations,
        system=system,
    )
