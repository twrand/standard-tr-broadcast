# Todo attribute this properly

import math

# Returns the (Manhattan) distance between two vertices on the infinite grid
def _dist(x1, y1, x2, y2):
	return abs(x1-x2) + abs(y1-y2)

# Returns the signal provided for a vertex v by a tower T
def _sig(t, vx, vy, Tx, Ty):
	return max(0, t - _dist(vx, vy, Tx, Ty))
	
# Returns a theoretical lower bound on the density of towers in 
# a standard (t,r) broadcast
def _getDMax(t,r):
	usable_signal = 0
	
	# Count 1 signal from each vertex v with sig(v,T) >=1
	# Count 2 signal from each vertex v with sig(v,T) >=2
	# ...
	# Count r signal from each vertex v with sig(v,T) >=r
	for t_rad in range(t, max(t-r,0), -1):
		usable_signal += _A(t_rad)

	return int(float(usable_signal) / r)

# Returns the number of vertices covered by a tower of signal strength t
def _A(t):
	return t*t + (t-1)*(t-1)
	
# Returns the minimum total signal at any vertex when towers in T(d,e) have
# signal strength t.
def _getMinSignalDepth(t, d, e):
	# Create the list of test vertices v_(0,0) ... v_(d-1,0) to be tested
	test_vertices = [0] * d
	
	# Sum the signal of all towers within a close window:
	# Test y values from -t+1 to t-1
	# Test x values from -t+1 to d+t-2
	for Ty in range(-t+1, t):
		for Tx in range(-t + 1, d+t-1):
		
			# Test if v_(x,y) \in T(d,e)
			# If so, account for signal.
			if ((Tx - e*Ty) % d == 0):
				# Increment signal recieved at each test vertex from this tower
				for vx in range(0,d):
					test_vertices[vx] += _sig(t, vx, 0, Tx, Ty)
	return min(test_vertices)

# Given a t,r standard broadcast, test all standard patterns up to the theoretical
# lower bound of density and return the standard broadcast of lowest density.
def getBestTRStandardBroadcast(t,r):
	d_opt = 0
	e_opt = 0

	for d in range(1, _getDMax(t,r) + 1):
		for e in range(d-1, -1, -1):
			if _getMinSignalDepth(t,d,e) >= r:
				d_opt = d
				e_opt = e
				
	print "Opt Std ("+str(t)+", "+str(r)+") broadcast is T("+str(d_opt)+","+str(e_opt)+") (density 1/"+str(d_opt)+")"

###############################################################################
# Call methods from here                                                      #
###############################################################################

getBestTRStandardBroadcast(4,5)