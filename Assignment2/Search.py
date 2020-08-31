import numpy as np
from queue import Queue
import os
from datetime import datetime
import math
from heapq import heappush,heapify,heappop,nsmallest
from scipy.spatial.distance import cityblock
import sys

class search():
    longitude_0_180 = {'0,0','30,0','60,0','90,0','120,0','150,0','180,180','150,180','120,180','90,180','60,180','30,180'}
    longitude_90_270 = {'0,0','30,90','60,90','90,90','120,90','150,90','180,180','150,270','120,270','90,270','60,270','30,270'}
    equator = {'90,0','90,30','90,60','90,90','90,120','90,150','90,180','90,210','90,240','90,270','90,300','90,330'}

    longitude_0 = [[0,0],[30,0],[60,0],[90,0],[120,0],[150,0],[180,180],[150,180],[120,180],[90,180],[60,180],[30,180]]
    longitude_90 = [[0,0],[30,90],[60,90],[90,90],[120,90],[150,90],[180,180],[150,270],[120,270],[90,270],[60,270],[30,270]]
    equator_2 = [[90,0],[90,30],[90,60],[90,90],[90,120],[90,150],[90,180],[90,210],[90,240],[90,270],[90,300],[90,330]]

    reached=0
    depth=0
    num_steps=0
    depth=0
    cost=0
    
    def increment_0(self,inputs,target):
        new=np.copy(inputs)
        for i in range(len(inputs)):
            if str(new[i][0])+','+str(new[i][1]) in self.longitude_0_180:
                if inputs[i][0]==150:
                    new[i][1] = 180

                if inputs[i][0]==30:
                    new[i][1] = 0

                if inputs[i][1]==0:
                    new[i][0] += 30

                if inputs[i][1]==180:
                    new[i][0] -= 30

                inputs[i]=new[i]

        self.num_steps+=1

        if inputs.tolist()==target.tolist():
            self.reached=1

        return inputs,self.reached

    def decrement_0(self,inputs,target):
        for i in range(len(inputs)):
            if str(inputs[i][0])+','+str(inputs[i][1]) in self.longitude_0_180:
                if inputs[i][0]==180:
                    inputs[i][1] = 0

                if inputs[i][0]==0:
                    inputs[i][1] = 180

                if inputs[i][1]==0:
                    inputs[i][0]-=30

                if inputs[i][1]==180:
                    inputs[i][0]+=30

        self.num_steps+=1
        if inputs.tolist()==target.tolist():
            self.reached=1

        return inputs,self.reached

    def increment_90(self,inputs,target):
        for i in range(len(inputs)):
            if str(inputs[i][0])+','+str(inputs[i][1]) in self.longitude_90_270:
                if inputs[i][0]==0 and inputs[i][1]==0:
                    inputs[i] = np.array([30,90])

                elif inputs[i][0]==180 and inputs[i][1]==180:
                    inputs[i] = np.array([150,270])

                elif inputs[i][1]==270:
                    inputs[i][0]-=30

                    if inputs[i][0]==0:
                        inputs[i][1]=0

                elif inputs[i][1]==90:
                    inputs[i][0]+=30

                    if inputs[i][0]==180:
                        inputs[i][1]=180

        self.num_steps+=1

        if inputs.tolist()==target.tolist():
            self.reached=1
        return inputs,self.reached

    def decrement_90(self,inputs,target):
        for i in range(len(inputs)):
            if str(inputs[i][0])+','+str(inputs[i][1]) in self.longitude_90_270:
                if inputs[i][0]==0 and inputs[i][1]==0:
                    inputs[i] = np.array([30,270])

                elif inputs[i][0]==180 and inputs[i][1]==180:
                    inputs[i] = np.array([150,90])

                elif inputs[i][1]==90:
                    inputs[i][0] -= 30

                    if inputs[i][0]==0:
                        inputs[i][1]=0

                elif inputs[i][1]==270:
                    inputs[i][0] += 30

                    if inputs[i][0] == 180:
                        inputs[i][1]=180

        self.num_steps+=1

        if inputs.tolist()==target.tolist():
                self.reached=1
        return inputs,self.reached

    def increment_e(self,inputs,target):
        for i in range(len(inputs)):
            if str(inputs[i][0])+','+str(inputs[i][1]) in self.equator:
                inputs[i][1] += 30

                if inputs[i][1]==360:
                    inputs[i][1]=0

        if inputs.tolist()==target.tolist():
                self.reached=1

        self.num_steps+=1
        
        return inputs,self.reached

    def decrement_e(self,inputs,target):
        for i in range(len(inputs)):
            if str(inputs[i][0])+','+str(inputs[i][1]) in self.equator:
                inputs[i][1] -= 30

                if inputs[i][1]==-30:
                    inputs[i][1]=330

        if inputs.tolist()==target.tolist():
                self.reached=1

        self.num_steps+=1
        
        return inputs,self.reached

    def bfs(self,current,target):
        final_path = []
        visited = {''}
        node = Queue()
        node.put(current)
        camefrom = {str(current):(0,'')}
            
        if np.array_equal(current,target)==True:
            return current,self.depth,self.num_steps,final_path,visited
        while(True):
            current = np.copy(node.get())
            
            visited.add(str(current))

            self.depth = math.ceil(math.log(self.num_steps+6,6))
            
            new_pos,reached = self.increment_0(np.copy(current),target)

            if reached==1:
                camefrom[str(new_pos)] = (current,'increment_0')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'increment_0')

            new_pos,reached = self.decrement_0(np.copy(current),target)
           
            if reached==1:
                camefrom[str(new_pos)] = (current,'decrement_0')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'decrement_0')

            new_pos,reached = self.increment_90(np.copy(current),target)
            
            if reached==1:
                camefrom[str(new_pos)] = (current,'increment_90')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'increment_90')

            new_pos,reached = self.decrement_90(np.copy(current),target)
            
            if reached==1:
                camefrom[str(new_pos)] = (current,'decrement_90')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'decrement_90')

            new_pos,reached = self.increment_e(np.copy(current),target)
            
            if reached==1:
                camefrom[str(new_pos)] = (current,'increment_e')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'increment_e')

            new_pos,reached = self.decrement_e(np.copy(current),target)
            
            if reached==1:
                camefrom[str(new_pos)] = (current,'decrement_e')
                temp = camefrom[str(new_pos)]
                while(True):
                    if temp[1]!='':
                        final_path.append(temp[1])
                        temp = camefrom[str(temp[0])]
                    else:
                        break
                    
                return new_pos,node.qsize(),final_path,visited

            if str(new_pos) not in visited:
                node.put(new_pos)
                camefrom[str(new_pos)] = (current,'decrement_e')


    def expand(self,current,target):
        new_pos,reached = self.increment_0(np.copy(current),target)
        
        expanded = new_pos.reshape(1,new_pos.shape[0],new_pos.shape[1])

        new_pos,reached = self.decrement_0(np.copy(current),target)
        expanded = np.insert(expanded,expanded.shape[0],new_pos,axis=0)

        new_pos,reached = self.increment_90(np.copy(current),target)
        expanded = np.insert(expanded,expanded.shape[0],new_pos,axis=0)
        
        new_pos,reached = self.decrement_90(np.copy(current),target)
        expanded = np.insert(expanded,expanded.shape[0],new_pos,axis=0)

        new_pos,reached = self.increment_e(np.copy(current),target)
        expanded = np.insert(expanded,expanded.shape[0],new_pos,axis=0)

        new_pos,reached = self.decrement_e(np.copy(current),target)
        expanded = np.insert(expanded,expanded.shape[0],new_pos,axis=0)
        
        return expanded

    def heuristic(self,node,target):
        
        distance = 0        
        for j in range(node.shape[0]):
            axis1 = axis2 = axis3 = Manhattan_dist = 0
            new = []
                        
            if str(node[j][0])+','+str(node[j][1]) in self.longitude_0_180 and str(target[j][0])+','+str(target[j][1]) in self.longitude_0_180:
                pos1 = [x for x in range(len(self.longitude_0)) if self.longitude_0[x][0] == node[j][0] and self.longitude_0[x][1] == node[j][1]][0]
                pos2 = [x for x in range(len(self.longitude_0)) if self.longitude_0[x][0] == target[j][0] and self.longitude_0[x][1] == target[j][1]][0]

                axis1 = 30*min([np.absolute(pos2 - pos1),len(self.longitude_0)-pos1+pos2,len(self.longitude_0)-pos2+pos1])

            if str(node[j][0])+','+str(node[j][1]) in self.longitude_90_270 and str(target[j][0])+','+str(target[j][1]) in self.longitude_90_270:
                pos1 = [x for x in range(len(self.longitude_90)) if self.longitude_90[x][0] == node[j][0] and self.longitude_90[x][1] == node[j][1]][0]
                pos2 = [x for x in range(len(self.longitude_90)) if self.longitude_90[x][0] == target[j][0] and self.longitude_90[x][1] == target[j][1]][0]

                axis2 = 30*min([np.absolute(pos2 - pos1),len(self.longitude_90)-pos1+pos2,len(self.longitude_90)-pos2+pos1])

            if str(node[j][0])+','+str(node[j][1]) in self.equator and str(target[j][0])+','+str(target[j][1]) in self.equator:
                pos1 = [x for x in range(len(self.equator_2)) if self.equator_2[x][0] == node[j][0] and self.equator_2[x][1] == node[j][1]][0]
                pos2 = [x for x in range(len(self.equator_2)) if self.equator_2[x][0] == target[j][0] and self.equator_2[x][1] == target[j][1]][0]

                axis3 = 30*min([np.absolute(pos2 - pos1),len(self.equator_2)-pos1+pos2,len(self.equator_2)-pos2+pos1])

            Manhattan_dist = np.absolute(target[j][0] - node[j][0]) + np.absolute(target[j][1] - node[j][1])
            if target[j][0] != node[j][0] or target[j][1] != node[j][1]:
                distance += min(x for x in [axis1,axis2,axis3,Manhattan_dist] if x>0)

        return distance/12
    
    def Astar(self,initial,target):

        open_list=[]
        camefrom = {str(initial):(0,'')}

        g_score = {str(initial):0}
        f_score = {str(initial):self.heuristic(np.copy(initial),target)}

        heappush(open_list,(f_score[str(initial)],0,initial))
        final_path = []
        max_queue = 0

        while(len(open_list) != 0):
            current = heappop(open_list)
            closed_list.add(str(current[2]))

            if current[2].tolist()==target.tolist():
                temp = camefrom[str(current[2])]
                while(temp[1] != ''):
                    final_path.append(temp[0])
                    temp = camefrom[temp[1]]

                final_path = ['increment_0' if x==1 else 'decrement_0' if x==2 else 'increment_90' if x==3 else 'decrement_90' if x==4 else 'increment_e' if x==5 else 'decrement_e' for x in final_path]
                return current[2],max_queue,final_path,closed_list

            expanded = self.expand(np.array(current[2]),target)

            for i in range(expanded.shape[0]):
                g_score[str(expanded[i])] = g_score[str(current[2])] + 30

                if str(expanded[i]) in closed_list:
                    continue
                    
                f_score[str(expanded[i])] = g_score[str(expanded[i])] + self.heuristic(np.copy(expanded[i]),target)

                heappush(open_list,(f_score[str(expanded[i])],self.num_steps + 0.0001 + i,expanded[i]))

                camefrom[str(expanded[i])] = (i,str(current[2]))

            if len(open_list)>max_queue:
                max_queue = len(open_list)
        
    def Rbfs(self,current,target,limit):
        if current.tolist() == target.tolist():
            reached = 1
            return 'Success',f_score[str(current)]

        expanded = self.expand(current,target)
        successors = []

        for i in range(expanded.shape[0]):
            g_score[str(expanded[i])] = g_score[str(current)] + 30
            f_score[str(expanded[i])] = max([f_score[str(current)],g_score[str(expanded[i])] + self.heuristic(np.copy(expanded[i]),target)])
            successors.append((f_score[str(expanded[i])],0.0001 + i + self.num_steps,expanded[i]))

            camefrom[str(expanded[i])] = (i,str(current))

        if len(successors) == 0:
            return 'failure',999999999
            
        successors = sorted(successors)
       
        while(True):
            bestNode = successors[0][2]

            if f_score[str(bestNode)]>limit:
                return 'failure',f_score[str(bestNode)]

            AltNode = successors[1][2]

            result,f_score[str(bestNode)] = self.Rbfs(np.copy(bestNode),target,min([limit,f_score[str(AltNode)]]))

            if result != 'failure':
                return result,f_score[str(bestNode)]
    

if __name__=='__main__':
    test_data=[]
    
    with open(sys.argv[2],"rt") as f:
        test_data.append(f.read().split('\n'))
    f.close()

    problems = []

    test_data[0].remove('<Marble>')
    test_data[0].remove('</Marble>')
    test_data[0].remove('')

    for j in range(len(test_data[0])):
        test_data[0][j] = test_data[0][j][5:]
        problems.append([np.array(test_data[0][j][test_data[0][j].find('(')+1:test_data[0][j].find(')')].split(','),dtype=np.int32),np.array(test_data[0][j][test_data[0][j].find('Exact(')+6:-2].split(','),dtype=np.int32)])

    problems = np.array(problems).reshape(30,4)
    move=search()

    closed_list = {''}
    current = np.copy(problems[:,:2])
    target = np.copy(problems[:,2:])

    if sys.argv[1] == 'BFS':
        ans,max_queue,final_path,visited = move.bfs(np.copy(current),target)

        print("Answer: ",ans)
        print("Max queue size: ",max_queue)
        print("Final path length: ",len(final_path))
        print("Number of explored nodes: ",len(visited))
        final_path.reverse()
        print("Final path: ",final_path)

    elif sys.argv[1] == 'AStar':
        ans,max_queue,final_path,visited = move.Astar(np.copy(current),target)

        print("Answer: ",ans)
        print("Max queue size: ",max_queue)
        print("Final path length: ",len(final_path))
        print("Number of explored nodes: ",len(visited))
        final_path.reverse()
        print("Final path: ",final_path)

    elif sys.argv[1] == 'RBFS':
        limit = 9999999
        f_score = {str(current):move.heuristic(np.copy(current),target)}
        g_score = {str(current):0}
        camefrom = {str(current):(0,'')}
        starttime = datetime.now()
        
        ans,ans_cost = move.Rbfs(current,target,limit)

        print("Answer: ",ans)
        print("Execution time: ",datetime.now()-starttime)
