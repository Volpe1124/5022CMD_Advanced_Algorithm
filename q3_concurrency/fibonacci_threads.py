import sys
import threading
import time

NUMBERS = (35, 38, 40)
ROUNDS = 10


def fibonacci(n):
    if n <= 1:                                   # base cases: F(0)=0, F(1)=1
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)   # two recursive calls


# ---------------------------------------------------------------------- #
# With multithreading
# ---------------------------------------------------------------------- #
class FibonacciThread(threading.Thread):

    def __init__(self, n):
        super().__init__(name=f"Fib-{n}")
        self.n = n
        self.result = None
        self.start_ns = None
        self.end_ns = None

    def run(self):
        self.start_ns = time.perf_counter_ns()   # t1 for this thread
        self.result = fibonacci(self.n)
        self.end_ns = time.perf_counter_ns()     # t2 for this thread


def run_with_threads():
    threads = [FibonacciThread(n) for n in NUMBERS]   # 3 separate threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()                                      # wait for all to finish
    first_start = min(t.start_ns for t in threads)
    last_end = max(t.end_ns for t in threads)
    results = {t.n: t.result for t in threads}
    return results, last_end - first_start            # T = t2 - t1


# ---------------------------------------------------------------------- #
# Without multithreading
# ---------------------------------------------------------------------- #
def run_without_threads():
    start = time.perf_counter_ns()
    results = {n: fibonacci(n) for n in NUMBERS}      # one after another
    end = time.perf_counter_ns()
    return results, end - start


# ---------------------------------------------------------------------- #
# Experiment driver
# ---------------------------------------------------------------------- #
def run_experiment(title, func):
    print(f"\n=== Fibonacci Computation ({title}) ===")
    times = []
    for r in range(1, ROUNDS + 1):
        results, elapsed = func()
        times.append(elapsed)
        values = ", ".join(f"Fib({n})={results[n]}" for n in NUMBERS)
        print(f"Round {r:>2}: {values} | T = {elapsed:>15,} ns")
    avg = sum(times) / len(times)
    print(f"Average T ({title}): {avg:,.0f} ns  (~{avg / 1e9:.2f} s)")
    return avg


def main():
    gil = "enabled"
    if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
        gil = "disabled (free-threaded build)"
    print(f"Python {sys.version.split()[0]} | GIL {gil} | {ROUNDS} rounds")

    avg_mt = run_experiment("With Multithreading", run_with_threads)
    avg_st = run_experiment("Without Multithreading", run_without_threads)

    diff = (avg_st - avg_mt) / avg_st * 100
    print("\n=== Summary ===")
    print(f"Average T with multithreading    : {avg_mt:>18,.0f} ns")
    print(f"Average T without multithreading : {avg_st:>18,.0f} ns")
    if diff > 0:
        print(f"Observation: Multithreading reduced the average time by {diff:.1f}%.")
    else:
        print(f"Observation: Multithreading was {-diff:.1f}% SLOWER "
              "(threads take turns because of the GIL).")


if __name__ == "__main__":
    main()
