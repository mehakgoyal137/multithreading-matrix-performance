import numpy as np
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import psutil
import csv
import os

# Matrix size optimized
N = 500  

# Setup paths relative to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, "../results")
os.makedirs(results_dir, exist_ok=True)

# Constant matrix
const_matrix = np.random.rand(N, N)

# Function to multiply one random matrix with constant
def multiply_once(_):
    rand_matrix = np.random.rand(N, N)
    return np.dot(rand_matrix, const_matrix)

def run_experiment(num_threads):
    start = time.time()
    # Reduced iterations to avoid memory crash
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(multiply_once, range(100)))  # 100 random matrices
    end = time.time()
    return (end - start) / 60  # minutes

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    max_threads = num_cores   # sir ke kehne ke hisaab se

    results = []
    for t in range(1, max_threads + 1):
        minutes = run_experiment(t)
        results.append((t, minutes))
        print(f"Threads={t}, Time={minutes:.2f} min")

    # Save results to CSV
    csv_path = os.path.join(results_dir, "execution_times.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Threads", "Time(min)"])
        writer.writerows(results)

    # Plot graph
    threads, times = zip(*results)
    plt.figure(1)
    plt.plot(threads, times, marker="o")
    plt.xlabel("Number of Threads")
    plt.ylabel("Time Taken (min)")
    plt.title("Execution Time")
    graph_path = os.path.join(results_dir, "execution_graph.png")
    plt.savefig(graph_path)
    plt.close()

    # CPU usage snapshot
    cpu_percent = psutil.cpu_percent(percpu=True)
    plt.figure(2)
    plt.bar(range(len(cpu_percent)), cpu_percent)
    plt.xlabel("CPU Core")
    plt.ylabel("Usage (%)")
    plt.title("CPU Usage Snapshot")
    cpu_path = os.path.join(results_dir, "cpu_usage.png")
    plt.savefig(cpu_path)
    plt.close()
    print(f"\nResults saved to: {results_dir}")
