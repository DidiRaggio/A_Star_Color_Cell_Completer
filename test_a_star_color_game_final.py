import numpy as np
import unittest
from a_star_color_game_final import State, StateStatus, AStar_Solver

class TestAStar(unittest.TestCase):


	#CREATE METHODS TO INITIALIZE TESTING EXAMPLES, BEFORE EACH TEST CASE
	def setUp(self):
		self.input_matrix = np.array([
			[0, 0, 1, 0, 0, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 1, 0, 1, 0, 0],
			[1, 0, 0, 1, 1, 1],
			[1, 0, 1, 1, 0, 1],
			[1, 0, 1, 0, 0, 0]
			])
		self.initialState = StateStatus([[0,0]], self.input_matrix,None)
		self.astar = AStar_Solver([[0,0]],self.input_matrix)
		self.sampleState  = State([[0,0]], self.input_matrix, None)
		self.aux_value =[
		[0, 0], 
		[1, 0], 
		[1, 1], 
		[1, 2], 
		[1, 3], 
		[0, 3], 
		[0, 1], 
		[2, 0], 
		[0, 2], 
		[2, 2], 
		[2, 3], 
		[0, 4], 
		[3, 0], 
		[0, 5], 
		[3, 1], 
		[3, 2], 
		[3, 3], 
		[4, 0], 
		[4, 1], 
		[3, 4], 
		[2, 1], 
		[1, 4], 
		[2, 4], 
		[1, 5], 
		[3, 5],
		[4, 4], 
		[4, 5],
		[5, 4]]

	def test_state(self):
		self.assertIsNone(self.sampleState.parent)
		self.assertEqual(self.sampleState.value, [[0,0]])
		self.assertIsInstance(self.sampleState, State)
		self.assertNotIsInstance(self.sampleState, StateStatus)

	def test_state_status(self):
		self.assertIsInstance(self.initialState, StateStatus)
		self.assertEqual(self.initialState.dist, 35)


	def test_state_status_get_dist(self):
		self.assertEqual(self.initialState.dist, 35)
		self.initialState.value = self.aux_value
		self.assertEqual(self.initialState.GetDist(), 8)
		self.assertNotEqual(self.initialState.dist, 8)

	def test_state_status_get_color_coords(self):
		ones = self.initialState.getColorCoords(self.input_matrix, 1)
		zeros = self.initialState.getColorCoords(self.input_matrix, 0)
		self.assertEqual(len(ones)+len(zeros), 36)
		self.assertIn([2,1], ones)
		self.assertIn([5,5], zeros)
		
	def test_state_status_get_available_neighbors(self):
		s = self.initialState
		bottom_right_corner = [[5,5]]
		left_side = [[3,0]]
		dougnut = [[1,1],[1,2],[1,3],[2,1],[2,3],[3,1],[3,2],[3,3]]
		self.assertEqual(len(s.getAvailableNeighbors(bottom_right_corner)), 2)
		self.assertEqual(len(s.getAvailableNeighbors(left_side)), 3)
		self.assertEqual(len(s.getAvailableNeighbors(dougnut)), 13)


	def test_state_status_get_value(self):
		s = self.initialState
		neighbors = s.getAvailableNeighbors([[0, 0],[0, 1],[1, 1]])
		# print(neighbors)
		# print(self.input_matrix[5][4])
		elements_of_that_color = s.getColorCoords(1, self.input_matrix)
		value = s.GetValue(neighbors,elements_of_that_color)
		# print(value)

	def test_state_status_create_children(self):

		self.assertEqual(self.initialState.children, [])
		# print("")
		self.initialState.CreateChildren()
		# print(self.initialState.color)
		new_children = self.initialState.children
		self.assertEqual(len(self.initialState.children), 3)
		# for child in new_children:
		# 	print("THE CHILD COLOR", child.color, "THE CHILD VALUE ",child.value)
		
		self.initialState.value = self.aux_value
		self.initialState.color = 1
		self.initialState.children = []
		self.initialState.CreateChildren()
		new_children2 = self.initialState.children
		# print("")
		# for child in new_children2:
			# print("THE CHILD COLOR", child.color, "THE CHILD VALUE ",child.value)
		self.assertEqual(len(self.initialState.children), 3)


		self.assertNotEqual(new_children, new_children2)

if __name__ == '__main__':
	unittest.main()
