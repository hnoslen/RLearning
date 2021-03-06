# R Learning
import numpy as np
class NaiveAgent:
	num_states = 0
	transitions = {}
	weights = np.array([[]])
	current_state = 0
	curious = True
	path = [0] # record of what states agent has passed through
	learning_rate = 0.005# 0.005
	step_propagation = 4 # must be greater than number of steps to that state
	reward_states = []
	punish_states = []
	end_states = []
	def states(self):
		return range(self.num_states)
	def initializeTransitions(self):
		self.transitions = {}
		for e in range(self.num_states):
			self.transitions[e] = set()
		return None
	def zeroWeights(self):
		self.weights = np.zeros((self.num_states,self.num_states), dtype=np.float)
		return self.weights
	def addTransition(self, from_state, to_state):
		if (((from_state <= self.num_states) and (from_state >= 0)) and ((to_state <= self.num_states) and (to_state >= 0))):
			self.transitions[from_state].add(to_state)
			return True
		else:
			return False
	def multiTransition(self, list_of_trans, directed):
		for e in list_of_trans:
			if (len(e)!= 2):
				return False
		for e in list_of_trans:
			if not directed:
				if (self.addTransition(e[0],e[1]) and self.addTransition(e[1],e[0])):
					continue
				else:
					return False
			else:
				if self.addTransition(e[0],e[1]):
					continue
				else:
					return False
		return True
	def removeTransition(self, from_state, to_state):
		if to_state in self.transitions[from_state]:
			self.transitions[from_state].remove(to_state)
			return True
		else:
			return False
	# Makes all weights 1 between connected states, 0 otherwise
	def startWeights(self):
		self.zeroWeights()
		for state in range(self.num_states):
			for conn in self.transitions[state]:
				self.weights[state][conn] = 1
		return self.weights
	def oneWeights(self):
		self.zeroWeights()
		for state in range(self.num_states):
			for conn in range(self.num_states):
				self.weights[state][conn] = 1
		return self.weights
	def __init__(self, nStates):
		self.num_states = nStates
		self.initializeTransitions()
		self.zeroWeights()
		return None
	def choose(self, state=None):
		if state==None:
			state = self.current_state
		copy_weights = self.weights[self.current_state].copy()
		if self.curious:
			copy_weights = (copy_weights>0)*1
			copy_weights = copy_weights.astype(float)
		copy_weights = copy_weights/copy_weights.sum()
		if copy_weights.sum()>0:
			return np.random.choice(copy_weights.size, 1, p=copy_weights)[0]
		else:
			raise ValueError("There aren't any possible state choices")
			return None
	def changeState(self, to_state):
		self.current_state = to_state
		self.path.append(self.current_state)
		return self.current_state
	def propagationEffect(self, method, steps_back):
		if method=='1/n':
			return self.learning_rate/steps_back
		elif method=='1/n^2':
			return self.learning_rate/(steps_back**2)
		else:
			return self.learning_rate
	def reward(self, learning_modifier):
		toReward = self.path[(-1*self.step_propagation):]
		i = 0
		while (i+1) < len(toReward):
			if self.weights[toReward[i]][toReward[i+1]]==0:
				pass
			else:
				self.weights[toReward[i]][toReward[i+1]] = (1+(learning_modifier*self.learning_rate))*self.weights[toReward[i]][toReward[i+1]]
			i = i+1
		return None
	def step(self):
		prev = self.current_state
		go_to = self.changeState(self.choose())
		if go_to in self.reward_states:
			self.reward(1)
		elif go_to in self.punish_states:
			self.reward(-1)
		else:
			pass
		return None
	def run(self):
		while self.current_state not in self.end_states:
			self.step()
			print self.current_state
		return (self.current_state, len(self.path))
	def resetStates(self):
		self.current_state = 0
		self.path = [0]
		return True
	def batchRun(self, iterations):
		i = 0
		end_conds = []
		while i < iterations:
			end_conds.append(self.run())
			self.resetStates()
			i = i+1
		return end_conds

# Is rewarded/punished for every move better or worse
class GreenerAgent:
	num_states = 0
	transitions = {}
	weights = np.array([[]])
	current_state = 0
	curious = True
	path = [0] # record of what states agent has passed through
	learning_rate = 0.005# 0.005
	step_propagation = 4 # must be greater than number of steps to that state
	reward_states = {}# must be pairs with desire value
	end_states = []
	def states(self):
		return range(self.num_states)
	def initializeTransitions(self):
		self.transitions = {}
		for e in range(self.num_states):
			self.transitions[e] = set()
		return None
	def zeroRewardStates(self):
		self.reward_states = {}
		for e in range(self.num_states):
			self.reward_states[e] = 0
		return self.reward_states
	def zeroWeights(self):
		self.weights = np.zeros((self.num_states,self.num_states), dtype=np.float)
		return self.weights
	def addTransition(self, from_state, to_state):
		if (((from_state <= self.num_states) and (from_state >= 0)) and ((to_state <= self.num_states) and (to_state >= 0))):
			self.transitions[from_state].add(to_state)
			return True
		else:
			return False
	def multiTransition(self, list_of_trans, directed):
		for e in list_of_trans:
			if (len(e)!= 2):
				return False
		for e in list_of_trans:
			if not directed:
				if (self.addTransition(e[0],e[1]) and self.addTransition(e[1],e[0])):
					continue
				else:
					return False
			else:
				if self.addTransition(e[0],e[1]):
					continue
				else:
					return False
		return True
	def removeTransition(self, from_state, to_state):
		if to_state in self.transitions[from_state]:
			self.transitions[from_state].remove(to_state)
			return True
		else:
			return False
	# Makes all weights 1 between connected states, 0 otherwise
	def startWeights(self):
		self.zeroWeights()
		for state in range(self.num_states):
			for conn in self.transitions[state]:
				self.weights[state][conn] = 1
		return self.weights
	def oneWeights(self):
		self.zeroWeights()
		for state in range(self.num_states):
			for conn in range(self.num_states):
				self.weights[state][conn] = 1
		return self.weights
	def __init__(self, nStates):
		self.num_states = nStates
		self.initializeTransitions()
		self.zeroWeights()
		self.zeroRewardStates()
		return None
	def choose(self, state=None):
		if state==None:
			state = self.current_state
		copy_weights = self.weights[self.current_state].copy()
		if self.curious:
			copy_weights = (copy_weights>0)*1
			copy_weights = copy_weights.astype(float)
		copy_weights = copy_weights/copy_weights.sum()
		if copy_weights.sum()>0:
			return np.random.choice(copy_weights.size, 1, p=copy_weights)[0]
		else:
			raise ValueError("There aren't any possible state choices")
			return None
	def changeState(self, to_state):
		self.current_state = to_state
		self.path.append(self.current_state)
		return self.current_state
	def propagationEffect(self, method, steps_back):
		if method=='1/n':
			return self.learning_rate/steps_back
		elif method=='1/n^2':
			return self.learning_rate/(steps_back**2)
		else:
			return self.learning_rate
	def reward(self, learning_modifier):
		toReward = self.path[(-1*self.step_propagation):]
		i = 0
		while (i+1) < len(toReward):
			if self.weights[toReward[i]][toReward[i+1]]==0:
				pass
			else:
				self.weights[toReward[i]][toReward[i+1]] = (1+(learning_modifier*self.learning_rate))*self.weights[toReward[i]][toReward[i+1]]
			i = i+1
		return None
	def step(self):
		prev = self.current_state
		go_to = self.changeState(self.choose())
		if go_to in self.reward_states:
			if self.reward_states[go_to] > self.reward_states[prev]:
				self.reward(1)
			elif self.reward_states[go_to] < self.reward_states[prev]:
				self.reward(-1)
			else:
				pass
		else:
			pass
		return None
	def run(self):
		while self.current_state not in self.end_states:
			self.step()
			print self.current_state
		return (self.current_state, len(self.path))
	def resetStates(self):
		self.current_state = 0
		self.path = [0]
		return True
	def batchRun(self, iterations):
		i = 0
		end_conds = []
		while i < iterations:
			end_conds.append(self.run())
			self.resetStates()
			i = i+1
		return end_conds
