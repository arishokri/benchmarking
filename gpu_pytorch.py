import torch
import time
from datetime import datetime
import os
import platform
from typing import Tuple


def get_platform_dependencies() -> (
    str
):  # Modify this to also distinguish between WSL and Linux runs.
    if platform.system() != "Darwin":
        import psutil
        import pynvml

        # Initialize NVML to access GPU stats
        pynvml.nvmlInit()
        return "non-darwin"
    else:
        return "darwin"


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


def get_gpu_temp() -> Tuple[int, int]:
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assumes the first GPU
    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    return temp, utilization


def get_cpu_temp() -> int:
    """
    This will only work on Linux
    On Linux, this reads temperatures from system sensors.
    psutil.sensors_temperatures() provides info if available.
    """
    temps = psutil.sensors_temperatures()
    if "coretemp" in temps:
        cpu_temp = temps["coretemp"][0].current  # Gets the first core temp
    else:
        cpu_temp = None
    return cpu_temp


def log_performance(logfile, test_duration=60, matrix_size=1024, iterations=10) -> None:
    plat = get_platform_dependencies()
    with open(logfile, "a") as f:
        f.write(
            "Timestamp, GPU Temp (°C), GPU Utilization (%), CPU Temp (°C), Matrix Time (s)\n"
        )
        start_time = time.time()
        # Perform matrix operation and log its duration
        while time.time() - start_time < test_duration:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if plat == "linux":
                gpu_temp, gpu_util = get_gpu_temp()
                cpu_temp = get_cpu_temp()
                torch_device = "cuda"
            elif plat == "darwin":
                gpu_temp = gpu_util = f"running on {plat}"
                cpu_temp = f"running on {plat}"
                torch_device = "mps"
            matrix_time = stress_gpu_with_matrix_operations(
                matrix_size=matrix_size,
                iterations=iterations,
                torch_device=torch_device,
            )
            # Get CPU and GPU metrics on systems that support them.
            # Log metrics
            log_entry = (
                f"{timestamp}, {gpu_temp}, {gpu_util}, {cpu_temp}, {matrix_time: .4f}\n"
            )
            # Optional, track memory release and allocation.
            #             allocated_bytes = torch.cuda.memory_stats_as_nested_dict()[
            #                 "allocated_bytes"
            #             ]["all"]
            #             print(
            #                 f"""
            # current bytes: {allocated_bytes["current"]}
            # total allocated: {allocated_bytes["allocated"]}
            # total freed: {allocated_bytes["freed"]}
            #             """
            #             )
            # torch.cuda.empty_cache()
            print(log_entry.strip())
            f.write(log_entry)
            # Wait for a number of seconds.
            time.sleep(2)


if __name__ == "__main__":
    duration = 300  # sets test duration in seconds
    matrix_size = 15000
    iterations = 100
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/pytorch_{duration}s"
    log_performance(
        logfile=log_file,
        test_duration=duration,
        matrix_size=matrix_size,
        iterations=iterations,
    )
