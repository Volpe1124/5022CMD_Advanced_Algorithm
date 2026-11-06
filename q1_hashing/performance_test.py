import random
import time

from hash_table import HashTable
from medicine import Medicine

SIZES = [100, 1_000, 5_000, 10_000]
REPEATS = 5
SEED = 42


def build_data(n):
    rng = random.Random(SEED)
    ids = rng.sample(range(100_000, 999_999), n)
    return [Medicine(pid, f"Medicine-{pid}", rng.uniform(1, 100),
                     rng.randint(0, 500)) for pid in ids]


def linear_search(array, product_id):
    for med in array:
        if med.product_id == product_id:
            return med
    return None


def measure(search_fn, keys):
    total = 0
    for _ in range(REPEATS):
        start = time.perf_counter_ns()
        for k in keys:
            search_fn(k)
        total += time.perf_counter_ns() - start
    return total / (REPEATS * len(keys))


def run():
    print("=== Search Performance: Hash Table vs One-Dimensional Array ===")
    print(f"(average time per search, {REPEATS} repetitions, every record searched)\n")
    print(f"{'Records':>8} | {'Hash Table (ns)':>15} | {'Avg probes':>10} | "
          f"{'Array (ns)':>12} | {'Speed-up':>9}")
    print("-" * 66)
    results = []
    for n in SIZES:
        data = build_data(n)
        table = HashTable(capacity=2 * n + 1)   # load factor ~0.5
        array = []
        for med in data:                        # same data in both structures
            table.put(med.product_id, med)
            array.append(med)

        keys = [m.product_id for m in data]
        random.Random(SEED).shuffle(keys)

        probe_total = 0
        for k in keys:
            table.get(k)
            probe_total += table.last_probes
        avg_probes = probe_total / n

        t_hash = measure(table.get, keys)
        t_array = measure(lambda k: linear_search(array, k), keys)
        results.append((n, t_hash, t_array))
        print(f"{n:>8,} | {t_hash:>15,.0f} | {avg_probes:>10.2f} | "
              f"{t_array:>12,.0f} | {t_array / t_hash:>8.1f}x")

    n, data = SIZES[-1], build_data(SIZES[-1])
    table = HashTable(2 * n + 1)
    for m in data:
        table.put(m.product_id, m)
    missing = 1                               # never generated (ids >= 100000)
    t_h = measure(table.get, [missing])
    t_a = measure(lambda k: linear_search(data, k), [missing])
    print(f"\nUnsuccessful search (ID not present, {n:,} records):")
    print(f"  Hash Table: {t_h:,.0f} ns   Array: {t_a:,.0f} ns")
    return results


if __name__ == "__main__":
    run()
