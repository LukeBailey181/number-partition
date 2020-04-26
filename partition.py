import sys
import random

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
for j in range(25000):
    Heap = MaxHeap(200)
    for i in range(100):
        Heap.add(random.randint(1,10**12))
    kk(Heap)
    if (j % 1000 == 0):
        print(j)
