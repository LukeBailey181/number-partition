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
    flag, alg = int(args[1]), int(args[2])
    in_file = args[3] if len(args) > 3 else None

    if flag == 0:
        problem = generateProblem(in_file)
    else:
        problem = storeNewProblem(in_file)

    if alg == 1: #implement other algs
        print(repeatedRandom(problem))

    elif alg == 2:
        print(hillClimber(problem)[0])

    elif alg == 3:
        print(simulatedAnnealing(problem)[0])

    else: #default to Karmarkar Karp
        H = MaxHeap(PROBLEM_SIZE * 2)
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

def randSolution():
    """
    Generate a random solution of signs
    """
    return random.choices([-1, 1], k=PROBLEM_SIZE)

def residue(problem=None, signs=None, heap=None):
    """
    generically get residue of a solution
    params problem, signs provide one approach
        lists of inputs and solution signs, respectively
    param heap alternative if kk variation used
        should have only one nonzero int rep. residue
    """
    res = 0
    if heap is None:
        for i in range(len(problem)):
            res += problem[i] * signs[i]
    else:
        res = heap.max()

    return abs(res)

def getSignsNeighbor(sol):
    """
    get random neighbor from a solution composed of signs sequence
    """
    signs = sol[:] #don't want to change sol, just generate new list
    i, j = random.sample(range(0, len(signs)), k=2)
    signs[i] = -signs[i]
    if random.choice([0, 1]) == 0:
        signs[j] = -signs[j]

    return signs


def repeatedRandom(problem):
    """
    repeatedly generate random solutions and return best
    """
    S = randSolution()
    minRes = residue(problem=problem, signs=S)
    for i in range(MAX_ITER):
        S_prime = randSolution()
        res_prime = residue(problem=problem, signs=S_prime)
        if(res_prime < minRes):
            #S = S_prime #make assignment if needed for return
            minRes = res_prime

    return minRes

def hillClimber(problem):
    """
    repeatedly generate improving random neighbors
    """
    S = randSolution()
    minRes = residue(problem=problem, signs=S)
    for i in range(MAX_ITER):
        S_prime = getSignsNeighbor(S)
        res_prime = residue(problem=problem, signs=S_prime)
        if(res_prime < minRes):
            minRes = res_prime
            S = S_prime

    return minRes, S

def simulatedAnnealing(problem):
    """
    move to neighbors, not necessarily better
    """
    S = randSolution()
    best = S
    bestRes = residue(problem, S)
    curr_res = bestRes
    
    for i in range(MAX_ITER):
        S_prime = getSignsNeighbor(S)
        res_prime = residue(problem, S_prime)
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

    def parentpos(self, i):
        return ((i-1)//2)

    def leaf(self, i):
        if (i <= self.size and i >= self.size//2):
            return True
        else:
            return False

    def swap(self, i, j):
        a = self.heap[i]
        b = self.heap[j]
        self.heap[i] = b
        self.heap[j] = a

    def add(self, number):
        if self.size >= self.maxsize:
            return
        self.size += 1
        index = self.size
        self.heap[index] = number

        while (self.heap[index] > self.heap[self.parentpos(index)]):
            parent = self.parentpos(index)
            self.swap(index, parent)
            index = parent


    def maxheapify(self,i):
        lchild = self.heap[self.leftchild(i)]
        rchild = self.heap[self.rightchild(i)]

        if (not self.leaf(i) and (self.heap[i] < lchild or self.heap[i] < rchild)):

            if (lchild > rchild):
                self.swap(i,self.leftchild(i))
                self.maxheapify(self.leftchild(i))

            else:
                self.swap(i,self.rightchild(i))
                self.maxheapify(self.rightchild(i))

    def max(self):

        max = self.heap[0]
        self.heap[0] = self.heap[self.size]
        self.size -= 1
        self.maxheapify(0)
        return(max)

    def Print(self):
        for i in range(1, (self.size//2)+1):
            print(" PARENT : "+str(self.heap[i])+" LEFT CHILD : "+
                               str(self.heap[2 * i])+" RIGHT CHILD : "+
                               str(self.heap[2 * i + 1]))
    def raw_print(self):
        print(self.heap)

def kk(heap):
    while (heap.size > 1):
        value1 = heap.max()
        value2 = heap.max()
        dif = value1 - value2
        heap.add(dif)
    return(heap.max())


#Heap.add(5)
##Heap.add(17)
#Heap.add(10)
#Heap.add(84)
#Heap.add(19)
#Heap.add(6)
#Heap.add(22)
#Heap.add(9)
"""
for j in range(25000):
    Heap = MaxHeap(200)
    for i in range(100):
        Heap.add(random.randint(1,10**12))
    kk(Heap)
    if (j % 1000 == 0):
        print(j)
"""

main()
