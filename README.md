# Symmetric-Weakly-Separated-Collection-Algorithm
Implements an algorithm to generate maximal symmetric weakly separated collections of subsets given parameters n, k, and l. Includes tools to compute orbits under modular shifts, validate input conditions, and verify set properties. Useful for research in combinatorics and relates to Legendrian weaves through T-shift. Note: this algorithm differs from the algorithm in our paper in that the algorithm in the paper removes duplicates, but this adaptation of the algorithm eschews that step for more seamless implementation. 


### Files and How to Use 

### generateSetsReduced.py

**Parameters:**

- n (int):
  - Total number of elements to choose from. Arithmetic is done modulo n (e.g., rotational symmetry).
- k (int ≤ n/2):
  - Size of each subset.
- l (int < n):
  - Symmetry parameter. The algorithm assumes a symmetry of d = n / gcd(n, l) blocks (roughly corresponding to angles of 2π/d radians).
- [override] (optional, set/list of length l):
  - A manual ordering of the elements {1, 2, ..., l}. 
  - When l does not divide n, the ordering must begin with the equivalence classes from g+1 to l and end with the equivalence classes from 1 to g. In other words, min{1, 2, ..., g} > max{g+1, g+2, ..., l}.
- [printSeeds] (optional, bool):
  - If `True`, prints the initial seed sets used to generate the full collection.
- [printCollection] (optional, bool):
  - If True, prints the entire generated maximal symmetric weakly separated collection.

**Parameter Conditions:**

For a successful set, we check:
- gcd(n,l) != 1
- k = {-1,0,1} mod n/gcd(n,l)
- l >= n / (k+1)
- k <= n/2
  - One can take the complement of the k=n-k case to achieve this result, may be added in a later fix

**Usage Syntax:**

- python generateSetsReduced.py n k l [override] [printSeeds] [printCollection]
- python generateSetsReduced.py 10 5 5 [3,2,1,4,5] True True
- Can be run directly from file if avoiding terminal use.


### generateSetsFull.py

**Requirements:** 
- If you want seeds copied to the clipboard, pyperclip is required.

**Parameters:**
- n (int):
  - Total number of elements to choose from. Arithmetic is done modulo n (e.g., rotational symmetry). If a single input, will generate a random collection up to size n. 
- k (int ≤ n/2):
  - Size of each subset.
- l (int < n):
  - Symmetry parameter. The algorithm assumes a symmetry of d = n / gcd(n, l) blocks (roughly corresponding to angles of 2π/d radians).
- [clipboard] (optional, bool):
  -  Default: False, no changes. If True, outputted generated collection will be copied to clipboard (useful is using a plabic tiling generator such as https://www.math.ucla.edu/~galashin/plabic.html)
- [override] (optional, set/list of length l):
  - A manual ordering of the elements {1, 2, ..., l}. 
  - When l does not divide n, the ordering must begin with the equivalence classes from g+1 to l and end with the equivalence classes from 1 to g. In other words, min{1, 2, ..., g} > max{g+1, g+2, ..., l}.
    
**Parameter Conditions:**

For a successful set, we check:
- gcd(n,l) != 1
- k = {-1,0,1} mod n/gcd(n,l)
- l >= n / (k+1)
- k <= n/2
  - One can take the complement of the k=n-k case to achieve this result, may be added in a later fix

**Usage Synatax:**

5 Parameters:
- python generateSetsFull.py n k l [clipboard] [override]
- python generateSetsFull.py 10 5 5 True [5,4,3,2,1]
  - Generates a collection using [5,4,3,2,1] ordering for n=10, k=5, l=5 and copies result to clipboard

4 Parameters:
- python generateSetsFull.py n k l [clipboard]
- python generateSetsFull.py 10 5 5 True
  - Generates a collection using a semi-random ordering for n=10, k=5, l=5 and copies result to clipboard

1 Parameter:
- python generateSetsFull.py n
- python generateSetsFull.py 10
  - Generate a random collection for an n from 4 to 10.

### generateSetsReducedManualInput.py

**Usage Syntax:**

- In a terminal, run generateSetsReducedManualInput.py 
- The data for n, k, l, and the ordering are taken from user input through the terminal, although the data is checked for failure conditions

