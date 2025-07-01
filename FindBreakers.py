import sys
from itertools import combinations
from math import gcd

def parse_input(raw, k):
    subsets = []
    for line in raw.strip().splitlines():
        nums = tuple(sorted(int(x) for x in line.strip().split()))
        if len(nums) == k:
            subsets.append(nums)
    return subsets

def between(x, y, z):
    return (x < y < z) or (z < x < y) or (y < z < x)

def interleave(a1, a2, b1, b2, n):
    return (between(a1, b1, a2) and between(a1, b2, a2)) or \
           (between(b1, a1, b2) and between(b1, a2, b2))

def weakly_separated_correct(A, B, n):
    A_minus_B = sorted(set(A) - set(B))
    B_minus_A = sorted(set(B) - set(A))
    combined = sorted(set(A_minus_B + B_minus_A))

    for i in range(len(combined)):
        for j in range(i + 1, len(combined)):
            for k in range(j + 1, len(combined)):
                for l in range(k + 1, len(combined)):
                    a, b, c, d = combined[i], combined[j], combined[k], combined[l]
                    if {a, c}.issubset(A_minus_B) and {b, d}.issubset(B_minus_A):
                        return False
                    if {a, c}.issubset(B_minus_A) and {b, d}.issubset(A_minus_B):
                        return False
    return True

def add_mod(subset, l, n):
    return tuple(sorted((x + l - 1) % n + 1 for x in subset))

def orbit(subset, l, n):
    result = []
    current = subset
    seen = set()
    for _ in range(n // gcd(n, l)):
        frozen = tuple(sorted(current))
        if frozen in seen:
            break
        seen.add(frozen)
        result.append(frozen)
        current = add_mod(current, l, n)
    return result

def is_weakly_separated_all(collection, n):
    for i in range(len(collection)):
        for j in range(i + 1, len(collection)):
            if not weakly_separated_correct(collection[i], collection[j], n):
                return False
    return True

def possible_orbit_extensions(current_collection, n, k, l):
    all_subsets = list(combinations(range(1, n + 1), k))
    used_orbits = {frozenset(orbit(sub, l, n)) for sub in current_collection}
    current_set = list(current_collection)
    max_size = k * (n - k) + 1

    valid_extensions = []
    for candidate in all_subsets:
        candidate_orbit = orbit(candidate, l, n)
        frozen_candidate_orbit = frozenset(candidate_orbit)

        if frozen_candidate_orbit in used_orbits:
            continue

        extended_collection = current_set + list(frozen_candidate_orbit)

        if len(extended_collection) > max_size:
            continue

        if is_weakly_separated_all(extended_collection, n):
            valid_extensions.append(candidate_orbit)

    return valid_extensions

def find_non_weakly_separated(subsets, n):
    bad_pairs = []
    conflict_map = {i: [] for i in range(len(subsets))}
    for i in range(len(subsets)):
        for j in range(i + 1, len(subsets)):
            A = subsets[i]
            B = subsets[j]
            if not weakly_separated_correct(A, B, n):
                bad_pairs.append((i, j, A, B))
                conflict_map[i].append(j)
                conflict_map[j].append(i)
    return bad_pairs, conflict_map

def parse_input_from_file(filename, k):
    with open(filename, 'r') as f:
        raw = f.read()
    return parse_input(raw, k)

def driver(raw_input=None, n=None, k=None, filename=None):
    if filename:
        subsets = parse_input_from_file(filename, k)
    else:
        subsets = parse_input(raw_input, k)
    bad_pairs, conflict_map = find_non_weakly_separated(subsets, n)

    # === Output ===
    print(f"Found {len(bad_pairs)} non-weakly-separated pairs.\n")

    # Show each subset and its conflicts
    for i, conflicts in conflict_map.items():
        if conflicts:
            print(f"Subset #{i+1} ({' '.join(map(str, subsets[i]))}) conflicts with:")
            for j in conflicts:
                print(f"    #{j+1}: {' '.join(map(str, subsets[j]))}")
            print()

    # Optional: list all bad pairs explicitly
    print("--- Summary of all bad pairs ---")
    for i, j, A, B in bad_pairs:
        print(f"#{i+1} ({' '.join(map(str, A))})  ×  #{j+1} ({' '.join(map(str, B))})")



if __name__ == "__main__":
    # Example usage:
    # python FindBreakers.py input.txt 5 3
    # Note: Expected format is requires each line to contains k integers representing a subset of size k
    # Example:
    # python FindBreakers.py "1 3 5\n2 4 5\n3 4 5" 5 3
    # Or manual: raw input = "1 3 5\n2 4 5\n3 4 5", n=5, k=3
    # Done by brute force, so not efficient for large n, k
    if len(sys.argv) == 4:
        filename = sys.argv[1]
        n = int(sys.argv[2])
        k = int(sys.argv[3])
        driver(n=n, k=k, filename=filename)
    else:
        raw_input = """
        1 3 5
        2 4 5
        3 4 5
        """
        n = 5
        k = 3
        driver(raw_input=raw_input, n=n, k=k)