import math
import cairo
import random

WIDTH, HEIGHT = 512, 512
no_of_cell_rows = 128
no_of_cell_cols = 128

def drawCell(x, y):
	ctx.rectangle(x*1.0/no_of_cell_rows, y*1.0/no_of_cell_cols, 
				  1.0/no_of_cell_rows, 1.0/no_of_cell_cols)
	ctx.fill()

steps = 1000
cells = []

for i in xrange(no_of_cell_rows):
	row = []
	for j in xrange(no_of_cell_cols):
		row.append(int(random.random()*2))
	cells.append(row)

def checkCell(x, y):
	state = cells[x][y]
	x_neighbors = filter(lambda r: r>=0 and r<no_of_cell_cols, [x-1, x, x+1])
	y_neighbors = filter(lambda r: r>=0 and r<no_of_cell_rows, [y-1, y, y+1])
	neighbors = [(p,q) for p in x_neighbors for q in y_neighbors if not (p==x and q==y)]
	live_neighbor_list = filter(lambda x:x==1, 
				     [cells[neighbor[0]][neighbor[1]] for neighbor in neighbors])
	live_neighbors = len(live_neighbor_list)
	
	if state==1:
		if live_neighbors<2:
			return 0
		elif live_neighbors==2 or live_neighbors==3:
			return 1
		elif live_neighbors>3:
			return 0
	else:
		if live_neighbors==3:
			return 1
		else:
			return 0
	
def simulate():
	global cells
	newcells = [cells[:] for row in cells]
	for i in xrange(no_of_cell_rows):
		for j in xrange(no_of_cell_cols):
			newcells[i][j] = checkCell(i,j)
	cells = newcells
	
for k in xrange(steps):
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
	ctx = cairo.Context(surface)
	ctx.scale(WIDTH, HEIGHT)

	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(0, 0, 1, 1)
	ctx.fill()
	
	ctx.set_source_rgb(1.0, 1.0, 1.0)
	for i in xrange(no_of_cell_rows):
		for j in xrange(no_of_cell_cols):
			if cells[i][j]:
				drawCell(i, j)

	surface.write_to_png("output/conway/conway_{}.png".format(str(k+1).zfill(4)))
	simulate()