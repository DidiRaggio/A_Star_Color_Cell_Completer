from queue import PriorityQueue
import numpy as np
import copy


m = 3
n = 6


class State(object):
	def __init__(self, value, matrix, parent):

		self.children = []
		self.parent = parent
		self.matrix = matrix
		self.value = value
		if parent:
			self.path = parent.path[:]
			self.path.append(value)
			self.color = None
		else:
			self.path = [value]
			self.color = matrix[0][0]

 
	def GetDist(self):
		pass
	def CreateChildren(self):
		pass




class StateStatus(State):

	def __init__(self, value, matrix, parent):
		super(StateStatus, self).__init__(value, matrix, parent)
		self.dist = self.GetDist()

	def GetDist(self):
		#check to see if we reached our goal
		if len(self.value) == self.matrix.size:
			return 0
		dist = self.matrix.size - len(self.value)
		return dist

	# GET ALL COORDINATES FOR EVERY ELEMENT OF A COLOR:
	def getColorCoords(self, color, matrix):
		return [list(x) for x in np.argwhere(matrix==color)]

	def getAvailableNeighbors(self, path):
		#GET ALL COMPARABLE ELEMENTS
		available_neighbors = []
		for element in path:
			i=element[0]
			j=element[1]
			neighbors = [[i,j-1],[i-1,j],[i,j+1],[i+1,j]]
			verified_neighbors = [x for x in neighbors if (x not in path and x[0] >= 0 and x[1] >= 0 and x[0] < self.matrix.shape[0] and x[1] < self.matrix.shape[1])]
			for neighbor in verified_neighbors:
				if neighbor not in available_neighbors:
					available_neighbors.append(neighbor)
		return available_neighbors


	def GetValue(self, neighbors, elements_of_that_color):

		value = copy.copy(self.value)
		done = False
		while done == False:
			non_available_neighbors = []
			for index, neighbor in enumerate(neighbors):

				if neighbor in elements_of_that_color:
					value.append(neighbor)
					neighbors = [x for x in self.getAvailableNeighbors(value) if x not in non_available_neighbors]
					break
				elif index == len(neighbors) -1 :
					done = True
					break
			if len(neighbors) == 0:
				done=True
				break
		return value



	def CreateChildren(self):
		
		if not self.children:
			colors = list(range(m))

			if self.parent is not None:
				colors.remove(self.color)			
			for next_color in colors:
				elements_of_that_color = self.getColorCoords(next_color, self.matrix)
				neighbors = self.getAvailableNeighbors(self.value)
				val =self.GetValue(neighbors, elements_of_that_color)
				child = StateStatus(val, self.matrix, self)
				child.color = next_color
				self.children.append(child)


class AStar_Solver:
	def __init__(self, start,matrix):
		self.path = []
		self.visitedQueue = []
		self.priorityQueue = PriorityQueue()
		self.start = start
		self.matrix = matrix


	# CHANGE ALL PATH TO CURRENT COLOR
	def updateMatrixByColor(self, color, path, matrix):
		new_matrix = np.copy(matrix)
		for element in path:
			new_matrix[element[0]][element[1]] = color
		return new_matrix




	def Solve(self):

		startState = StateStatus(self.start, self.matrix,None)
		count = 0
		self.priorityQueue.put((0, count, startState))
		while(not self.path and self.priorityQueue.qsize()):
			closestChild = self.priorityQueue.get()[2]
			closestChild.CreateChildren()
			self.visitedQueue.append(closestChild.value)
			for child in closestChild.children:
				if child.value not in self.visitedQueue:
					count += 1
					if not child.dist:
						self.path = child.path
						break
					self.priorityQueue.put((child.dist,count, child))
		if not self.path:
			print( "Goal is not possible!")
		return self.path


if __name__ == "__main__":

	input_matrix = np.random.randint(m, size=(n,n))

	start1 = [[0,0]]
	print( "starting...")
	a = AStar_Solver(start1,input_matrix)
	a.Solve()
	for i, item in enumerate(a.path):
		value = a.path[i]
		print("")
		print("Path item ", i)
		print(value)
		print("COLOR:")
		color = a.matrix[a.path[i][-1][0]][a.path[i][-1][1]]
		print(color)
		print(a.updateMatrixByColor(color, value, a.matrix))

	print( "")
	print("THE ORIGINAL MATRIX")
	print(a.matrix)
