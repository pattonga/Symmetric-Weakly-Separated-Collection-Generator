from itertools import combinations
from math import gcd
from typing import Iterable, List, Sequence, Tuple
import random
import io
import sys
import pyperclip


# ───────────────────────
# Various Helper Functions
# ───────────────────────
def orbit(subset: Sequence[int], l, n, verbose) -> List[Tuple[int, ...]]:
    # Adjust *l* to 1 for the canonical consecutive seed
    if list(subset) == list(range(1, len(subset) + 1)):
        l = 1

    result: List[Tuple[int, ...]] = []
    current = tuple(subset)
    seen = set()

    for _ in range(n // gcd(n, l)):
        frozen = tuple(sorted(current))
        if frozen in seen:
            break
        seen.add(frozen)
        result.append(frozen)

        if verbose:
            print(*frozen)

        current = add_mod(current, l, n)

    return result

def add_mod(subset: Sequence[int], l: int, n: int) -> Tuple[int, ...]:
    return tuple(sorted(((x + l - 1) % n) + 1 for x in subset))

def checkConds(n,k,l, verbose):
    if gcd(n, l) == 1:
        if verbose:
            print("Failed GCD")
        return False
    p = gcd(n, l)
    modulus = n // p
    if k % modulus not in {modulus - 1, 0, 1}:
        if verbose:
            print(f"Failed K Modulus. k is congruent to {k%modulus} mod n//p ")          
        return False
    if k > n / 2:
        if verbose:
            print("Failed K <= n/2")  
        return False
    if l < n / (k + 1):
        if verbose:
            print("Failed l<n/(k+1)")  
        return False
    return True

def makeMapBetween(n, k, l):
    g=gcd(n,l)
    DictionNtoDL = {}
    for a in range(1,g+1):
        x=0
        while a+x*g <= n:
            nVerson = a+x*g
            dlVerson = a+x*l
            DictionNtoDL[dlVerson] = nVerson
            x+=1
            
    return DictionNtoDL
    
# ───────────────────────
# Main Algorithm
# ───────────────────────
def Valgorithm2(n, k, l, verbose, stOrder=True,override=[]):

# ───────────────────────
# Initialization of variables
# ───────────────────────

    g = gcd(n, l)
    d= n//g
    gcdFix = False
    if l != g:
        fixMap = makeMapBetween(n,k,l)
        gcdFix = True
        prevN = n
        n = d*l
        #l = gcd(prevN,l)
    seen_orbits = set()                         # Keeps track of orbits already found so we are not redundant
    total_Available = set(range(1, n + 1))      # all elements from 1 to n excluding non a terms in a equivalence class
    previousStepRemoval = set(range(1, n + 1))  # Updated at end of Bi. Does not contain any element from previous Bi
    seedsList:    List[Tuple[int, ...]] = []    # Keeps all seeds
    tooSmall = False                            # Break condition when we run out of terms throughout the code
    removedFromRight = False                    # Keeps track if we removed from right of a_i (term in [l]) or from the left

    if stOrder:
        ordering= list(range(1,l+1))  # Just a list from 1 to n for ordering purposes
        ordering.reverse()
        print("Standard ordering:", ordering)
    elif not stOrder and gcdFix:
        print(g)
        ordering = []
        avNums = list(range(g+1,l+1))
        while avNums != []:
            pick = random.choice(avNums)
            avNums.remove(pick)
            ordering.append(pick)
        avNums = list(range(1,g+1))
        avNums.reverse()
        for i in avNums:
            ordering.append(i)
        #while avNums != []:
        #    pick = random.choice(avNums)
        #    avNums.remove(pick)
        #    ordering.append(pick)
        print("Random ordering:", ordering)
    else:
        ordering = []
        avNums = list(range(1,l+1))
        while avNums != []:
            pick = random.choice(avNums)
            avNums.remove(pick)
            ordering.append(pick)
        print("Random ordering:", ordering)
    if override != []:
        ordering = override
        print("Override ordering:", ordering)
    

# ───────────────────────
# Main loop
# ───────────────────────
    startAt = l-g
    print(f"Starting at bucket {startAt} (l-g={l}-{g}). Now n={n}, k={k}, l={l}, g={g}.")
    for i in range(0,startAt):                  # Remove all buckets before l-g
        #a=l-i
        a = ordering[i]
        j=1
        while (a+j*l-1)%n+1 != a:                               # Remove a and its equivalence class from previousStepRemoval
                previousStepRemoval.discard((a+j*l-1)%n+1)
                j+=1
        previousStepRemoval.discard(a)
    total_Available = previousStepRemoval.copy()  # Set total_Available to be the same as previousStepRemoval
    
    for i in range(startAt,l):                  # iterate through buckets. For now this assumed l < l-1 < l-2 < ... < 1 (a=l-i in setup)

        # ───────────────────────
        # Set up loop variables
        # ───────────────────────
        #a=l-i                                   # Force choice to obey l<l-1<l-2<...
        a=ordering[i]                            # Choose a based on ordering


        orbitA = []                             # Variable to keep track of what is in equivalence class of a that is not a
        left = []                               # Left half of seed (what comes before a)
        right = []                              # Right half of seed (a and after)
        outOfTerms=False                        # Track variable to know if there are any terms we might remove in the right 
        
        # ───────────────────────
        # Set up orbitA and Total_Available for this bucket
        # ───────────────────────                       

        j=1
        while (a+j*l-1)%n+1 != a:
            orbitA.append((a+j*l-1)%n+1)        #Add all non a elemenets in a's equivalence class
            total_Available.discard((a+j*l-1)%n+1) #Remove non a elements from Available pool
            j+=1

        # ───────────────────────
        # Generate all sequencial based on available terms in previousStepRemoval
        # ───────────────────────

        iterConsecs =  []                        # Sets to iterate on (all consecutive)
        ordered = sorted(previousStepRemoval)   # Puts them into sorted order
        print(ordered)
        for u in range(len(ordered)):           # Loop through sequences
            base = (a-k-1)%n+1
            while (base+1-1)%n+1 not in previousStepRemoval:  # (base+1-1)%n+1 = Find sucessor to a-k
                base = (base+1-1)%n+1
            start = ordered.index((base+1-1)%n+1)
            print(start)
            consec = tuple(ordered[(start + j+u) % len(ordered)] for j in range(k))     # Create the consecutive  terms 
            iterConsecs.append(consec)                                                  # Add this to a the iterate set 
            if(consec[0])== a:                                                          # We are done when a starts on the left
                break

        # ───────────────────────
        # Begin loop for all consecutive numbers
        # ───────────────────────
        print(f"Consecutive sets for bucket {a}: {iterConsecs}")
        for consec in iterConsecs:             

            candidate = tuple(consec)
            orbit_repr = tuple(sorted(orbit(candidate, l, n, verbose=False)))

            if orbit_repr not in seen_orbits:
                seen_orbits.add(orbit_repr)
                seedsList.append(candidate)


            # ───────────────────────
            # Construct Left and Right for this starting seed
            # ───────────────────────
            j=0
            left=[]
            right=[]
            while consec[j]!= a:
                left.append(consec[j])                      # Construct left until we reach a
                j+=1
            while j<k:
                right.append(consec[j])                     # Starting at a, finish off right so that left+right has size k
                j+=1
            for r in right:                                 # See if we will be starting by removing from right (this impacts while loop when left = [] to start)
                if r not in total_Available:
                    outOfTerms = False

            if verbose:
                print(f"Current consecutive seed for bucket {a}: Left = {left} Right = {right}")     # If we are printing, give some starter details

            # ───────────────────────
            # Main removal loop given a starting seed
            # ───────────────────────
            while (not outOfTerms or left != []):   # While there are terms to iterate on (if we can shift from left or have things on right)
                if len(previousStepRemoval)==k:     # No items to add, so we are done
                    break
                if(tooSmall):                       # Break condition when things underflow
                    break
                removedFromRight = False
        

                # ───────────────────────
                # Removing a certain elemenet
                # ───────────────────────
                
                if not outOfTerms:
                    for i in range(len(right)):         # Try to remove an element from the right side
                        r = right[(len(right)-1)-i]     # Iterate from right to left in the right list
                        if r not in total_Available:    # If r is in the equivalence class for a
                            removedFromRight = True     
                            right.remove(r)             # Remove r
                            break
                if not removedFromRight:                # If we did not remove from the right, we remove from the left (we can assume there will be one by initial check)    
                    left.remove(left[0])

                # ───────────────────────
                # Adding a new elemenet to the right
                # ───────────────────────

                if removedFromRight:                    # If we removed from right and it was in the equivalence class (so we add to the end)
                    last = right[len(right)-1]
                    j = 1
                    while (last+j-1)%n+1 not in total_Available or (last+j-1)%n+1 in left+right:
                        j += 1
                        if(j> n):                       # Break condition if no consecutive to add
                            print("100 overflow")
                            tooSmall = True
                            break
                    if tooSmall:
                        break
                    right.append((last+j-1)%n+1)        # Add the next consecutive non-equivalence class element into right
                else:
                    fillGap = False
                    if(len(right)>2):                   # Look for gaps in right to fill first
                        fillGap = False
                        for index in range(len(right)-1):
                            if right[index+1] == (right[index] + 1-1)%n+1:  # If next is present, skip (short case)
                                continue
                            else:
                                j=1

                                while (((right[index] + j-1)%n+1 not in previousStepRemoval) or ((right[index] + j-1)%n+1 in (left+right))):     #Check if there is a consectuvie  missing not in either left or right
                                    if (right[index] + j-1)%n+1 == right[index+1]:  # If we reach the next element, break
                                        break
                                    j+=1
                                if ((right[index] + j-1)%n+1 in previousStepRemoval) and ((right[index] + j-1)%n+1 not in (left+right)):
                                    right.append((right[index] + j-1)%n+1)
                                    right.sort()
                                    fillGap = True
                                    break
                                else:
                                    continue 
                                
                    if not fillGap:                              # If no gaps, add the next consecutive non-equivalence class element into right
                        last = right[len(right)-1]
                        j = 1
                        while last+j not in previousStepRemoval: #Loop to find available term
                            j += 1
                        right.append(last + j)                   # Add term
                if verbose:
                    print("After filling right hole:", left, right)

                # ───────────────────────
                # Add seed and set up for next iteration
                # ───────────────────────


                outOfTerms = True
                for r in right:                                  # Check if we have terms to remove in the right
                    if r not in total_Available:
                        outOfTerms = False
                    
                candidate = tuple(sorted(left + right))
                orbit_repr = tuple(sorted(orbit(candidate, l, n, verbose=False)))

                if orbit_repr not in seen_orbits:
                    seen_orbits.add(orbit_repr)                 # Add new seed if we have not seen it before
                    seedsList.append(candidate)
        
        j=1
        while (a+j*l-1)%n+1 != a:                               # Remove a and its equivalence class from previousStepRemoval
            previousStepRemoval.discard((a+j*l-1)%n+1)
            j+=1
        previousStepRemoval.discard(a)
        if verbose:
            print(previousStepRemoval)
        total_Available.discard(a)                              # Variable cleanup with discarding
        if(len(previousStepRemoval) < k):                       # Check if we have another bucket
            break
    
    if gcdFix:                                  # If we changed n and l at the start, we need to fix the seeds
        print(fixMap)
        newSeedsList = []
        for seed in seedsList:
            newSeed = []
            for s in seed:
                newSeed.append(fixMap[s])
            newSeedsList.append(tuple(sorted(newSeed)))
        seedsList = newSeedsList
        n=prevN
    if verbose:
        print("\nBegin list of seeds:\n")                       # Print seeds if we are in verbose mode
        for seed in seedsList:
            print(seed)
        print("\nEnd list of seeds:\n")
        print("\nBegin generating collection:\n")

        output = ""  # To collect all the prints

        for seed in seedsList:
            buffer = io.StringIO()
            sys.stdout = buffer  # Redirect print statements

            orbit(seed, l, n, verbose=True)  # Prints go to buffer now

            sys.stdout = sys.__stdout__  # Reset stdout
            output += buffer.getvalue()
            buffer.close()
        pyperclip.copy(output)  # Send to clipboard
        print(output)
        print("\nEnd generating collection:\n")
    return seedsList

# ---------------------------------------------------------------------------
# Tester
# ---------------------------------------------------------------------------
def test_valgorithm2_up_to(startN, max_n: int, *, quiet_valgo: bool = True,
                           verbose: bool = False, supPass=False) -> None:

    import contextlib, io, sys

    # ANSI escape helpers ---------------------------------------------------
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    RESET  = "\033[0m"

    def colour(txt: str, clr: str) -> str:
        return f"{clr}{txt}{RESET}" if sys.stdout.isatty() else txt

    def suppress_output():
        return (contextlib.redirect_stdout(io.StringIO())
                if quiet_valgo else contextlib.nullcontext())

    # -----------------------------------------------------------------------
    failures: list[tuple] = []
    counter = 0
    for n in range(startN, max_n + 1):
        for k in range(2, n - 1):
            for l in range(2, n-1):
                try:
                    if not checkConds(n, k, l, False):
                        continue  # silently skip invalid triples
                    if gcd(n, l) == l:
                        continue

                    with suppress_output():
                    #print(f"Testing n={n}, k={k}, l={l}...", end=' ')
                        counter+=1
                        seeds = Valgorithm2(n, k, l, verbose=not quiet_valgo, stOrder=False)

                    # independently rebuild the collection
                    unique_subsets = set()
                    for seed in seeds:
                        unique_subsets.update(orbit(seed, l, n, verbose=False))

                    expected = k * (n - k) + 1
                    found    = len(unique_subsets)
                    passed   = (found == expected)

                    if verbose:
                        if passed:
                            if not supPass:
                                status = colour("✓ PASS ", GREEN)
                                print(f"{status} n={n:2d}, k={k:2d}, l={l:2d} → {found:3d} / {expected}")
                        else:
                            status = colour("✗ FAIL ", RED)
                            print(f"{status} n={n:2d}, k={k:2d}, l={l:2d} → {found:3d} / {expected}")

                    if not passed:
                        failures.append((n, k, l, expected, found))

                except Exception as e:
                    failures.append((n, k, l, "exception", str(e)))
                    if verbose:
                        status = colour("! ERROR", YELLOW)
                        print(f"{status} n={n:2d}, k={k:2d}, l={l:2d} → {e}")

    # -----------------------------------------------------------------------
    if failures:
        print(f"\n❌ {len(failures)} failure(s) found up to n = {max_n}. Total cases = {counter}\n")
    else:
        print(colour(f"\n✔ All tests passed for every valid (n, k, l) triple with n ≤ {max_n}",
                     GREEN))


if __name__ == "__main__":
    nStart = 7
    n = 6
    k = 3
    l = 3
    override = [2,1]
    testing = False
    printRes = True
    randomTrial = False

    
    if testing:
        test_valgorithm2_up_to(nStart, n, quiet_valgo=True, verbose=True, supPass=False)
    elif randomTrial:
        conds = False
        while not conds:
            n = random.randint(4,90)
            l=random.randint(2,n-2)
            k=random.randint(2,n//2)
            conds = checkConds(n,k,l, False)
        print(f"We are going with n={n}, k={k}, l={l}.")
        seeds=Valgorithm2(n,k,l,printRes)
        unique_subsets = set()
        for seed in seeds:
            unique_subsets.update(orbit(seed, l, n, verbose=False))

        expected = k * (n - k) + 1
        found    = len(unique_subsets)
        print(found)
        print(expected)
    else:
        if(checkConds(n, k, l, True)):
            seeds=Valgorithm2(n,k,l,printRes, stOrder=True,override=override)
            unique_subsets = set()
            for seed in seeds:
                unique_subsets.update(orbit(seed, l, n, verbose=False))

            expected = k * (n - k) + 1
            found  = len(unique_subsets)
            print(found)
            print(expected)
        else:
            print(f"Invalid parameters: n={n}, k={k}, l={l}. Check conditions.")

        
        