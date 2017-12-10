import math

def ghost_proximity(results, world):
	if results[0] == results[1][0] or  results[0] == results[2][0]:
		val = -1
	else:
		val = 1
		#red_dist = math.sqrt( (p_y - r_y)**2 + (p_x - r_x)**2 )/10.
		#green_dist = math.sqrt( (p_y - gr_y)**2 + (p_x - gr_x)**2 )/10.
		#val = min(red_dist, green_dist)

	return val

def will_eat_dot(results, world):
	if results[3]:
		return 1
	else:
		return 0

def dot_proximity(results, world):

	x, y = results[0]

	dist_list = []

	if len( world.dots ) > 1: 
		for dx, dy in world.dots:
			if not (dx == x and dy == y):
				dist_list.append( math.sqrt( (y - dy)**2 + (x - dx)**2 ) )

		return (min(dist_list) / max(dist_list)) * 2.5
	elif len( world.dots ) == 1:
		sum_val = 0.0

		for dx, dy in world.dots:
			sum_val += math.sqrt( (y - dy)**2 + (x - dx)**2 )
		
		return sum_val
	else:
		return 0 

def ghost_proximity_beta(results, world):
	if results[0] == results[1][0] or  results[0] == results[2][0]:
		val = 1
	else:
		val = 0

	return val

def will_eat_dot_beta(results, world):
	if results[3]:
		val = 1
	else:
		val = 0

	return val

def dot_starve_prox(results, world):

	y, x = results[0]

	dist_list = []

	val = 0

	if ( not results[3] ) and world.dots: 
		for dy, dx in world.dots:
			if not (dx == x and dy == y):
				dist = abs(dy - y) + abs(dx - x)

				if dist not in dist_list:
					dist_list.append( dist )

		if dist_list:
			val = min(dist_list)/max(dist_list)

	return val

def pac_explore(results, world):
	y, x = results[0]
	max_val = max( max(world.pacmult) )

	if max_val == 0 or results[3]:
		val = 0
	else:
		val = world.pacmult[y][x] / max_val
	return val

feature_func = [ghost_proximity_beta, will_eat_dot_beta, pac_explore]
feature_names = {ghost_proximity_beta : "Ghost Proximity", will_eat_dot_beta : "Will Eat Dot", pac_explore : "Starve & Explore"}

def get_default_vector():
	return [-12.57, 3.94, -7.62]
	return [0, 0, 0]

def render_fvector(scr, fvector):
	fcount = min( len(feature_func), len(fvector) )

	xShift = 22
	yShift = 5

	scr.addstr(yShift - 1, xShift, "Weights: ")
	scr.addstr(yShift + fcount + 1, xShift, "Original Value and Distance")

	origin_vec = get_default_vector()

	for i in range(fcount):
		strang = feature_names[ feature_func[i] ]
		strang = strang + (": %.2f" % ( fvector[i] )) + (" " * 5) 

		scr.addstr(yShift + i, xShift, strang)

		strang = feature_names[ feature_func[i] ]
		strang = strang + (": %.2f (%.2f)" % ( origin_vec[i], fvector[i] - origin_vec[i] )) + (" " * 5) 

		scr.addstr(yShift + fcount + i + 2, xShift, strang)

