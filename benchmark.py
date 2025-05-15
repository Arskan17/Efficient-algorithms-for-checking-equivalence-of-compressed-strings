import psutil
import time
import subprocess
import fib_prod_G1
import fib_prod_G2

# Function to monitor resource usage
def monitor_resources(process, duration, interval=0.1):
    cpu_percentages = []
    memory_usages = []

    for _ in range(int(duration / interval)):
        # Record CPU and memory usage
        cpu_percentages.append(process.cpu_percent(interval=interval))
        memory_usages.append(process.memory_info().rss / (1024 * 1024))  # Convert bytes to MB

    # Calculate averages
    avg_cpu = sum(cpu_percentages) / len(cpu_percentages) if cpu_percentages else 0
    avg_memory = sum(memory_usages) / len(memory_usages) if memory_usages else 0

    return avg_cpu, avg_memory


if __name__ == '__main__':
    i_th_fib_string = 300
    # G1
    fib_prod_G1.m(i_th_fib_string)  # Generate Fibonacci grammar for G1
    # G2
    fib_prod_G2.m(i_th_fib_string)  # Generate Fibonacci grammar for G2

    # Start timing
    start_time = time.time()

    # Start monitoring resources
    process = psutil.Process()

    try:
        # Run the main application script using subprocess
        subprocess.run(['python3', 'app.py'], check=True)
    finally:
        # End timing
        end_time = time.time()

        # Calculate execution duration
        duration = end_time - start_time

        # Calculate average CPU and memory usage
        avg_cpu, avg_memory = monitor_resources(process, duration)

        # Print results
        print(f"Execution time: {duration:.4f} seconds")
        print(f"Average CPU usage: {avg_cpu:.2f}%")
        print(f"Average RAM usage: {avg_memory:.2f} MB")