import matplotlib.pyplot as plt
import math
import random

def calc_disdis(node1, node2):
	dx = node1[0] - node2[0]
	dy = node1[1] - node2[1]

	return dx * dx + dy * dy

def calc_distance(node1, node2):
	return math.sqrt(calc_disdis(node1, node2))

class Group:
	def __init__(self):
		self.xvect = []
		self.yvect = []
	
	def add_node(self, node):
		self.xvect.append(node[0])
		self.yvect.append(node[1])

	def set_node(self, n, node):
		self.xvect[n] = node[0]
		self.yvect[n] = node[1]

	def get_node(self, n):
		return (self.xvect[n], self.yvect[n]);

	def get_center(self):
		if len(self.xvect) == 0 or len(self.yvect) == 0:
			print "Error: empty vector"
			return (0, 0)
		xcent = sum(self.xvect) / (float)(len(self.xvect))
		ycent = sum(self.yvect) / (float)(len(self.yvect))
		return (xcent, ycent)
	
	def add_group(self, group):
		self.xvect.extend(group.xvect)
		self.yvect.extend(group.yvect)
	
	def length(self):
		return len(self.xvect)

class Kmean:
	def __init__(self):
		self.cents = Group()
		self.datags = []
		self.itercnt = 0

	def add_center(self, node):
		self.cents.add_node(node)
	
	def add_data(self, group):
		self.datags.append(group)

	def init_groups(self):
		return [Group() for i in range(self.cents.length())]
	
	def add_groups(self, a, b):
		for i in range(len(a)):
			a[i].add_group(b[i])

	def compare_dist(self, node):
		"""
		Find center point which having minimal distance
		"""

		min = 9999999
		idx = -1
		for i in range(self.cents.length()):
			dis = calc_disdis(self.cents.get_node(i), node)
			if dis < min:
				min = dis
				idx = i

		return idx
	
	def cluster_group(self, group):
		"""
		Cluster group by determinating the distance of each center point
		"""

		clusteredgs = [Group() for i in range(self.cents.length())]

		for i in range(group.length()):
			node = group.get_node(i)
			which = self.compare_dist(node)
			clusteredgs[which].add_node(node)

		return clusteredgs

	def calc_center(self, groups):
		ret = Group()
		for i in range(len(groups)):
			cent = groups[i].get_center()
			ret.add_node(cent)

		return ret
	
	def draw_plot(self, cents, new_cents, groups, optmsg = ""):
		"""
		Draw center point, new center point and each group
		"""

		plt.title("k-mean it=%d (%s)" % (self.itercnt, optmsg))
		plt.axis([0, 30, 0, 30])

		param = ("ro", "bo", "co", "ko", "go", "mo")

		for i in range(len(groups)):
			plt.plot(groups[i].xvect, groups[i].yvect, param[i])

		plt.plot(new_cents.xvect, new_cents.yvect, "mo", ms=10)
		plt.plot(cents.xvect, cents.yvect, "yo", ms=10)

		for i in range(cents.length()):
			plt.plot([new_cents.xvect[i], cents.xvect[i]], [new_cents.yvect[i], cents.yvect[i]], "k-")

		plt.show()
		

	def check_stop(self, new_cents):
		"""
		Check if new center point differs from old center point
		"""

		is_stop = True
		for i in range(new_cents.length()):
			disdis = calc_disdis(self.cents.get_node(i), new_cents.get_node(i))
			if disdis > 0.00001:
				is_stop = False
				break

		return  is_stop
	
	def calc_sse(self):
		sse = 0

		for i in range(self.cents.length()):
			center = self.cents.get_node(i)
			for j in range(self.datags[i].length()):
				sse = sse + calc_distance(center, self.datags[i].get_node(j))

		return sse


	def report_sse(self):
		print "SSE: %d" % self.calc_sse()


	def main(self):
		MAX_ITERATION = 20

		while True and self.itercnt < MAX_ITERATION:

			self.draw_plot(self.cents, self.cents, self.datags, "INITIAL")

			resultgs = self.init_groups()
			for i in range(len(self.datags)):
				tempgs = self.cluster_group(self.datags[i])	
				self.add_groups(resultgs, tempgs)

			new_cents = self.calc_center(resultgs)
			self.draw_plot(self.cents, new_cents, resultgs, "CLUSTERED")

			self.itercnt = self.itercnt + 1

			if self.check_stop(new_cents):
				self.cents = new_cents
				self.report_sse();
				break

			self.cents = new_cents
			self.report_sse();
		

if __name__ == "__main__":

	MAX_TEST_GROUPS = 5
	MAX_TEST_NODES = 35

	test_data = []

	for i in range(MAX_TEST_GROUPS):
		group = Group()
		for j in range(MAX_TEST_NODES):
			node = (random.randint(0, 30), random.randint(0, 30))
			group.add_node(node)
		test_data.append(group)

	"""
	c1 = (5.0, 15.0)
	c2 = (15.0, 5.0)
	c3 = (25.0, 15.0)
	c4 = (15.0, 25.0)
	"""
	c1 = (random.randint(5, 25), random.randint(5, 25))
	c2 = (random.randint(5, 25), random.randint(5, 25))
	c3 = (random.randint(5, 25), random.randint(5, 25))
	c4 = (random.randint(5, 25), random.randint(5, 25))


	kmean = Kmean()

	kmean.add_center(c1)
	kmean.add_center(c2)
	kmean.add_center(c3)
	kmean.add_center(c4)

	for i in range(MAX_TEST_GROUPS):
		kmean.add_data(test_data[i])

	kmean.main()

