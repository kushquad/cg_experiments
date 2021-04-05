import math
import cairo
import random

WIDTH, HEIGHT = 512, 512
no_of_cell_rows = 16
no_of_cell_cols = 16

def drawCell(x, y, col):	
	ctx.set_source_rgb(col[0]/255.0, col[1]/255.0, col[2]/255.0)
	ctx.rectangle(x*1.0/no_of_cell_rows, y*1.0/no_of_cell_cols, 
				  1.0/no_of_cell_rows, 1.0/no_of_cell_cols)
	ctx.fill()

steps = 1000
cells = []

for i in xrange(no_of_cell_rows):
	row = []
	for j in xrange(no_of_cell_cols):
		row.append(random.random())
	cells.append(row)

def getLiveNeighbors(x, y):
	x_neighbors = filter(lambda r: r>=0 and r<no_of_cell_cols, [x-1, x, x+1])
	y_neighbors = filter(lambda r: r>=0 and r<no_of_cell_rows, [y-1, y, y+1])
	neighbors = [(p,q) for p in x_neighbors for q in y_neighbors if not (p==x and q==y)]
	live_neighbor_list = filter(lambda x:x>0.97, 
				     [cells[neighbor[0]][neighbor[1]] for neighbor in neighbors])
	live_neighbors = len(live_neighbor_list)
	return live_neighbors
	
def checkCell(x, y):
	live_neighbors = getLiveNeighbors(x, y)
	state = cells[x][y]
	
	if state>0.95:
		if live_neighbors<1:
			return 0.95*state
		elif live_neighbors==1 or live_neighbors==2:
			return 1.05*state
		elif live_neighbors>2:
			return 0.95*state
	else:
		if 0<live_neighbors<=2:
			return ((1+0.05*live_neighbors)*state)
		else:
			return 0.95*state
	
def simulate():
	global cells
	newcells = [cells[:] for row in cells]
	for i in xrange(no_of_cell_rows):
		for j in xrange(no_of_cell_cols):
			newcells[i][j] = checkCell(i,j)
	cells = newcells

def colorMap(color_idx):
	return [(0, 173, 241), 
			(226, 232, 158),
			(104, 182, 72),
			(82, 142, 168),
			(104, 182, 72),
			(132, 148, 174),
			(123, 137, 163),
			(221, 243, 241),
			(254, 254, 254)][color_idx]
	
for k in xrange(steps):
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
	ctx = cairo.Context(surface)
	ctx.scale(WIDTH, HEIGHT)

	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(0, 0, 1, 1)
	ctx.fill()
	
	for i in xrange(no_of_cell_rows):
		for j in xrange(no_of_cell_cols):
			if cells[i][j]:
				drawCell(i, j, colorMap(getLiveNeighbors(i,j)))#cells[i][j]>0.85)

	surface.write_to_png("output/modified_conway/conway_{}.png".format(str(k+1).zfill(4)))
	simulate()