import sys
import random
from math import exp

#MACROS
PROBLEM_SIZE = 100 #number of ints in problem array
RAND_MAX = 10**12 #largest int in array
MAX_ITER = 25000 #number of times randomized algorithms will attempt to improve
COOLING_COEF = 10**10


def main():
    args = sys.argv
    flag, alg = int(args[1]), args[2]
    in_file = args[3] if len(args) > 3 else None

    if flag == 0:
        problem = generateProblem(in_file)
    else:
        problem = storeNewProblem(in_file)

    sol_type = "signs" if len(alg) == 1 else "prepartition"

    alg = int(alg[len(alg)-1])

    if alg == 1: #implement other algs
        print(repeatedRandom(problem, sol_type))

    elif alg == 2:
        print(hillClimber(problem, sol_type)[0])

    elif alg == 3:
        print(simulatedAnnealing(problem, sol_type)[0])

    else: #default to Karmarkar Karp
        H = MaxHeap(PROBLEM_SIZE)
        for val in problem:
            H.add(val)

        print(kk(H))



def storeNewProblem(in_file="numbers.txt"):
    """
    generate new random problem and store in in_file for replication
    """
    problem = generateProblem()
    raw = open(in_file, "w")
    for num in problem:
        raw.write(str(num) + "\n")
    raw.close()
    return problem

def generateProblem(in_file=None):
    """
    fill array with 100 'random' integers
    :param in_file optional file of integer inputs; default none
    """
    A = [0] * PROBLEM_SIZE #create problem input array A
    if in_file is None:
        for i in range(len(A)):
            A[i] = random.randint(0, RAND_MAX) #fill with non-negative int
    else:
        f = open(in_file, "r")
        for i in range(len(A)):
            A[i] = int(f.readline())
        f.close()

    return A

def randSolution(sol_type="signs"):
    """
    Generate a random solution of signs
    """
    return Solution.randomSolution(sol_type)


def kk(heap):
    while (heap.size > 1):
        value1 = heap.max()
        value2 = heap.max()
        dif = value1 - value2
        heap.add(dif)
    return(heap.max())

def repeatedRandom(problem, sol_type="signs"):
    """
    repeatedly generate random solutions and return best
    """
    S = randSolution(sol_type)
    minRes = S.residue(problem)
    for i in range(MAX_ITER):
        S_prime = randSolution(sol_type)
        res_prime = S_prime.residue(problem)
        if(res_prime < minRes):
            #S = S_prime #make assignment if needed for return
            minRes = res_prime

    return minRes

def hillClimber(problem, sol_type="signs"):
    """
    repeatedly generate improving random neighbors
    """
    S = randSolution(sol_type)
    minRes = S.residue(problem)
    for i in range(MAX_ITER):
        S_prime = S.getNeighbor()
        res_prime = S_prime.residue(problem)
        if(res_prime < minRes):
            minRes = res_prime
            S = S_prime

    return minRes, S

def simulatedAnnealing(problem, sol_type="signs"):
    """
    move to neighbors, not necessarily better
    """
    S = randSolution(sol_type)
    best = S
    bestRes = S.residue(problem)
    curr_res = bestRes
    
    for i in range(MAX_ITER):
        S_prime = S.getNeighbor()
        res_prime = S_prime.residue(problem)
        if res_prime < curr_res or random.random() < exp(-(res_prime - curr_res)/cooling(i)):
            S = S_prime
            curr_res = res_prime
        if curr_res < bestRes:
            best = S
            bestRes = curr_res

    return bestRes, best


def cooling(curr_iter):
    return COOLING_COEF * (0.8 **(curr_iter/300))


class MaxHeap:

    def __init__(self,maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.heap = [0] * (self.maxsize)

    def leftchild(self, i):
        return ((2 * i) + 1)

    def rightchild(self, i):
        return ((2 * i) + 2)

    def children(self, i):
        return self.leftchild(i), self.rightchild(i)

    def parentpos(self, i):
        return ((i-1)//2)

    def leaf(self, i):
        return (i < self.size and i >= self.size//2-1)

    def exists(self, i):
        return (i < self.size and i >= 0)

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i] 

    def add(self, number):
        if self.size >= self.maxsize:
            return
        self.size += 1
        index = self.size - 1
        self.heap[index] = number

        while (self.exists(self.parentpos(index)) and self.heap[index] > self.heap[self.parentpos(index)]):
            parent = self.parentpos(index)
            self.swap(index, parent)
            index = parent

    def maxheapify(self,i):
        
        l, r = self.children(i)
        max_idx = l if self.exists(l) and self.heap[l] > self.heap[i] else i
        if self.exists(r) and self.heap[r] > self.heap[max_idx]:
            max_idx = r

        if(max_idx != i):
            self.swap(max_idx, i)
            self.maxheapify(max_idx)

    def max(self):

        mx = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.maxheapify(0)
        return(mx)

    def isHeap(self):
        for i in range(0, self.size):
            l, r = self.children(i)
            if(self.exists(l) and self.heap[l] > self.heap[i] or (self.exists(r) and self.heap[r] > self.heap[i])):
                print("====================")
                print("Not a heap")
                print("Misplaced index at " + str(i))
                self.Print()
                print("====================")
                return False
        return True

    def Print(self):
        for i in range(1, (self.size//2)+1):
            print(" PARENT : "+str(self.heap[i])+" LEFT CHILD : "+
                               str(self.heap[2 * i])+" RIGHT CHILD : "+
                               str(self.heap[2 * i + 1]))
    def raw_print(self):
        print(self.heap)

class Solution:
    """
    Abstract parent class for two solution types
    """
    def __init__(self):
        self.sequence = []

    def randomSolution(sol_type):
        if sol_type == "signs":
            return SignSequence()
        elif sol_type == "prepartition":
            return Prepartition()

    def set(self, index, val):
        self.sequence[index] = val


class SignSequence(Solution):
    """
    Solution comprised of sequence of +-1 ints
    """
    def __init__(self, sequence=None):
        if sequence is None:
            self.sequence = random.choices([-1, 1], k=PROBLEM_SIZE)
        else:
            self.sequence = sequence[:]

    def getNeighbor(self):
        neighbor = SignSequence(self.sequence)
        i, j = random.sample(range(0, len(self.sequence)), k=2)
        neighbor.set(i, -self.sequence[i])
        if random.random() < 0.5:
            neighbor.set(j, -self.sequence[j])

        return neighbor

    def residue(self, problem):
        res = 0
        for i in range(len(problem)):
            res += problem[i] * self.sequence[i]

        return abs(res)

class Prepartition(Solution):
    """
    Solution comprised of prepartition
    """
    def __init__(self, sequence=None):
        if sequence is None:
            self.sequence = random.choices(range(0, PROBLEM_SIZE), k=PROBLEM_SIZE)
        else:
            self.sequence = sequence[:]

    def getNeighbor(self):
        neighbor = Prepartition(self.sequence)
        while(True):
            i, j = random.choices(range(0, len(self.sequence)), k=2)
            if(self.sequence[i] != j):
                neighbor.set(i, j)
                break

        return neighbor

    def residue(self, problem):
        partitioned = [0] * len(problem)
        for i in range(len(problem)):
            p_index = self.sequence[i]
            partitioned[p_index] += problem[i]

        H = MaxHeap(200)
        for val in partitioned:
            H.add(val)

        return kk(H)

main()
