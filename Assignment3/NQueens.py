from queue import Queue
from datetime import datetime
import sys

class Nqueen:
    board = []
    domain = {}
    solution = []
    var = []
    assignment = []
    
    def __init__(self,N,algo):
        self.N = N
        self.count = 0
        self.algo = algo
        self.num_backtracks = 0
        
        for i in range(N):
            self.board.append([0 for x in range(N)])
            self.domain[i] = set([x for x in range(N)])
            self.solution.append(0)

        self.var = [x for x in range(N)]

    def check(self, row, col):
        #Function to check whether current assignment is valid or not
        for i in range(row):
            if self.board[i][col] == 1:
                return False
                    
            if col - (row - i)>=0:
                if self.board[i][col - (row - i)] == 1:
                    return False
                    
            if col + (row - i)<self.N:
                if self.board[i][col + (row - i)] == 1:
                    return False
        return True

    def forward_check(self,row,col):
        valid = True
        
        #Maintain a list of removed values from domain so the domain can be restored during backtracking
        removed = []
        for i in range(row+1,self.N):
            if col in self.domain[i]:
                removed.append([i,col])
                self.domain[i].remove(col)

        #lower diagonal on left side 
        for i, j in zip(range(row+1, self.N, 1),range(col-1, -1, -1)):
            if j in self.domain[i]:
                removed.append([i,j])
                self.domain[i].remove(j)

        #lower diagonal on right side 
        for i, j in zip(range(row+1, self.N, 1),range(col+1, self.N, 1)):
            if j in self.domain[i]:
                removed.append([i,j])
                self.domain[i].remove(j)

        if 0 in [len(self.domain[x]) for x in self.domain.keys()]:
            valid = False
        return valid,removed

    def MAC(self,row,col):
        q = Queue()

        #Maintain a list of removed values from domain so the domain can be restored during backtracking
        removed = []
        neighbours = [x for x in range(self.N)]
        for i in range(row+1,self.N):
            q.put((i,row))

        #Reduce domain of assigned variable to the assigned value only
        for k in self.domain[row]:
            if k != col:
                removed.append([row,k])

        self.domain[row] = set([col])
        
        while not q.empty():
            Xi,Xj = q.get()
            revised,removed = self.Revise(Xi,Xj,removed)
            #Contraint propagation
            if revised:
                if len(self.domain[Xi])==0:
                    return False,removed
                for Xk in neighbours:
                    if Xk > row and Xk != Xi and Xk != Xj:
                        q.put((Xk,Xi))

        return True,removed

    def Revise(self,Xi,Xj,removed):
        revised = False
        for x in self.domain[Xi].copy():
            flag = [True for y in self.domain[Xj] if x != y and x != y - (Xi - Xj) and x != y + (Xi - Xj)]
            
            if len(flag) == 0:
                removed.append([Xi,x])
                self.domain[Xi].remove(x)
                revised = True

        return revised,removed

    def display(self):
        #Function to write the chess board to RFILE after placing N queens correctly
        with open(sys.argv[4]+".txt","a") as f:
            f.write("Solution "+str(self.count)+": "+str(self.assignment)+"\n")
            for i in range(self.N):  
                for j in range(self.N): 
                    f.write(str(self.board[i][j])+" ") 
                f.write("\n") 
            f.write("\n")
        f.close()

    def backtrack(self):
        if len(self.assignment) == self.N:
            self.count += 1
            self.display()
            return True

        if self.count>=2*self.N:
            return False

        variable = len(self.assignment)
        for val in self.domain[variable]:
            if self.check(variable, val):
                self.assignment.append(val)
                self.board[variable][val] = 1

                #Pass the current assignment to inference function
                success,removed = self.inference(variable,val)

                if success:
                    result = self.backtrack()

                #Remove currently assigned value, and restore changes made to domain by current assignment
                self.assignment.remove(val)
                self.board[variable][val] = 0
                self.restore(removed)

        #Update backtrack count
        self.num_backtracks += 1
        return False

    def inference(self,row,col):
        if self.algo == 'FOR':
            return self.forward_check(row,col)
        else:
            return self.MAC(row,col)

    def restore(self,removed):
        #Function to restore changes made to domain by current assignment
        for x,y in removed:
            self.domain[x].add(y)

if __name__ == "__main__":
    #Create instance of problem as 'QueenGraph'
    QueenGraph = Nqueen(N = int(sys.argv[2]),algo = sys.argv[1])
    open(sys.argv[4]+".txt","w")

    #Generate CFILE
    with open(sys.argv[3]+".txt","w") as f2:
        f2.write("Variables: "+str(QueenGraph.var)+"\n\n")
        for i in range(QueenGraph.N):
            f2.write("Domain "+str(i)+": "+str(QueenGraph.domain[i])+"\n")
        f2.write('\nConstraints:\n')
        for i in range(QueenGraph.N):
            for j in range(i+1,QueenGraph.N):
                f2.write('Q'+str(i)+' != Q'+str(j)+', |Q'+str(i)+' - Q'+str(j)+'| != '+str(abs(i-j))+'\n')
                
    f2.close()
    
    starttime = datetime.now()
    res = QueenGraph.backtrack()

    print("Number of solutions found: ",QueenGraph.count)
    print("Execution time: ",datetime.now()-starttime)
    print("Number of backtracks: ",QueenGraph.num_backtracks)

    with open(sys.argv[4]+".txt","a") as f1:
        f1.write("Number of solutions found: "+str(QueenGraph.count))
        f1.write("\nExecution time: "+str(datetime.now()-starttime))
        f1.write("\nNumber of backtracks: "+str(QueenGraph.num_backtracks))

    f1.close()
