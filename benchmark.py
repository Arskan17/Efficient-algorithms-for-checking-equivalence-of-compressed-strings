import psutil
import time
import subprocess
import threading
import fib_prod_G1
import fib_prod_G2
import csv
import os
import tqdm

def monitor_resources(process, running_flag, interval=0.001):
    """
    Monitor CPU and memory usage of a process.
    Args:
        process (psutil.Process): The process to monitor.
        running_flag (list): A list containing a single boolean value to control the monitoring loop.
        interval (float): Time interval between resource checks in seconds. Default is 0.001 seconds(1 millisecond).
    """
    cpu_percentages = []
    memory_usages = []
    while running_flag[0]:
        try:
            cpu_percentages.append(process.cpu_percent(interval=interval))
            memory_usages.append(process.memory_info().rss / (1024 * 1024))  # MB
        except psutil.NoSuchProcess:
            break  # The process ended
    avg_cpu = sum(cpu_percentages) / len(cpu_percentages) if cpu_percentages else 0
    avg_memory = sum(memory_usages) / len(memory_usages) if memory_usages else 0
    return avg_cpu, avg_memory

if __name__ == '__main__':
    # fib_string_num = [1,2,4,8,16,32,64,128,256,512]
    # for nu in fib_string_num:
        i_th_fib_string = 250
        fib_prod_G1.m(i_th_fib_string)
        fib_prod_G2.m(i_th_fib_string)
        dataset = 32

        for i in tqdm.tqdm(range(dataset)):
            running_flag = [True]
            results = {}

            # Start the subprocess and get its PID
            child = subprocess.Popen(['python3', 'app.py'])
            process = psutil.Process(child.pid)

            def monitor():
                avg_cpu, avg_memory = monitor_resources(process, running_flag)
                results['cpu'] = avg_cpu
                results['mem'] = avg_memory

            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()

            start_time = time.time()
            try:
                child.wait()
            finally:
                end_time = time.time()
                running_flag[0] = False
                monitor_thread.join()

                duration = end_time - start_time
                avg_cpu = results.get('cpu', 0)
                avg_memory = results.get('mem', 0)

                print(f"Execution time of the {i_th_fib_string}-th Fibonacci word: {duration:.4f} seconds")
                print(f"Average CPU usage: {avg_cpu:.2f}%")
                print(f"Average RAM usage: {avg_memory:.2f} MB")

            csv_file = "benchmark_results.csv"
            fieldnames = ["fib_index", "duration_sec", "avg_ram_mb"]

            # Check if file exists to write header only once
            write_header = not os.path.exists(csv_file)

            with open(csv_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow({
                    "fib_index": i_th_fib_string,
                    "duration_sec": duration,
                    "avg_ram_mb": avg_memory
                })

            time.sleep(0.1)  # Sleep for a short time to avoid cuncurrent processes