from itertools import combinations
from math import gcd
from typing import Iterable, List, Sequence, Tuple
import random
import sys
import ast

# ───────────────────────
# Helper Functions
# ───────────────────────
def orbit(subset: Sequence[int], l, n, verbose) -> List[Tuple[int, ...]]:
    """Like :func:`orbit2`, but optionally prints each element of the orbit."""
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
    """Add *l* (mod *n*) to every element of *subset*, renumbering to 1‑based."""
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
# Main Algorithm and runner
# ───────────────────────
def Valgorithm2(n, k, l, printSeeds=True, printCollection=True, stOrder=True,override=[]):

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
        ordering = []
        avNums = list(range(g+1,l+1))
        while avNums != []:
            pick = random.choice(avNums)
            avNums.remove(pick)
            ordering.append(pick)
        avNums = list(range(1,g+1))
        avNums.reverse()
        #for i in avNums:
        #    ordering.append(i)
        while avNums != []:
            pick = random.choice(avNums)
            avNums.remove(pick)
            ordering.append(pick)
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
        for u in range(len(ordered)):           # Loop through sequences
            base = ordered.index(a)
            base = (base - k+1)%len(ordered)  # Find the base for the consecutive terms (a-k+1)
            start = base
            consec = tuple(ordered[(start + j+u) % len(ordered)] for j in range(k))     # Create the consecutive  terms 
            iterConsecs.append(consec)                                                  # Add this to a the iterate set 
            if(consec[0])== a:                                                          # We are done when a starts on the left
                break

        # ───────────────────────
        # Begin loop for all consecutive numbers
        # ───────────────────────
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
            outOfTerms = True                            # Assume we are out of terms to remove from right
            for r in right:                                 # See if we will be starting by removing from right (this impacts while loop when left = [] to start)
                if r not in total_Available:
                    outOfTerms = False
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
        total_Available.discard(a)                              # Variable cleanup with discarding
        if(len(previousStepRemoval) < k):                       # Check if we have another bucket
            break
    
    if gcdFix:                                  # If we changed n and l at the start, we need to fix the seeds
        newSeedsList = []
        for seed in seedsList:
            newSeed = []
            for s in seed:
                newSeed.append(fixMap[s])
            newSeedsList.append(tuple(sorted(newSeed)))
        seedsList = newSeedsList
        n=prevN
    if printSeeds:
        print("\nBegin list of seeds:\n")                       # Print seeds if we are in verbose mode
        for seed in seedsList:
            print(seed)
        print("\nEnd list of seeds:\n")
    if printCollection:
        print("\nBegin generating collection:\n")

        for seed in seedsList:
            orbit(seed, l, n, verbose=True)  # Prints go to buffer now
        print("\nEnd generating collection:\n")
    return seedsList

def runAlgorithm(n, k, l, override=[], printSeeds=True, printCollection=True):
    """Run the Valgorithm2 algorithm with the given parameters."""
    if(checkConds(n, k, l, True)):
        seeds=Valgorithm2(n,k,l,printSeeds=printSeeds, printCollection=printCollection, stOrder=False,override=override)
        unique_subsets = set()
        for seed in seeds:
            unique_subsets.update(orbit(seed, l, n, verbose=False))

        expected = k * (n - k) + 1
        found  = len(unique_subsets)
        print(found)
        print(expected)
    else:
        print(f"Invalid parameters: n={n}, k={k}, l={l}. Check conditions.")


# ───────────────────────
# Main
# ───────────────────────

if __name__ == "__main__":
    # Example usage:
    # python generateSetsReduced.py n k l [override] [printSeeds] [printCollection]
    # python generateSetsReduced.py 10 4 6
    if (len(sys.argv) > 2):
        # If command line arguments are provided, use them
        n = int(sys.argv[1])
        k = int(sys.argv[2])
        l = int(sys.argv[3])
        override = ast.literal_eval(sys.argv[4]) if len(sys.argv) > 4 else []
        if not isinstance(override, list):
            print("Override must be a list of integers. Using empty list instead.")
            override = []
        else:
            if len(override) != l:
                print(f"Override list length {len(override)} does not match l={l}. Using empty list instead.")
                override = []
        printSeeds = True if len(sys.argv) < 6 or sys.argv[5].lower() == 'true' else False
        printCollection = True if len(sys.argv) < 7 or sys.argv[6].lower() == 'true' else False
    else:
        # Manual Run: Adjust and run from here
        n = 22      # Total number of elements
        k = 2       # Size of each subset
        l = 11       # Symmetry (Expect d=n/gcd(n, l) blocks of symmetry ~ 2pi/d))
        override = []   # Manual input for ordering, if needed. Note if gcd(n,l) != l, this may not work as expected.
        printSeeds = True # Print results or not
        printCollection = True # Print the collection generated or not
        
    runAlgorithm(n, k, l, override, printSeeds, printCollection)


        
        