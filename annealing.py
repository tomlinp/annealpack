from simanneal import Annealer
from shapely import geometry, affinity
from random import uniform

# returns a suggested (possibly overlapping) placement for a tile
def placeTile(pgon, bounds):
    # translate
    pgon = affinity.translate(
        geom = pgon,
        xoff = uniform(0, bounds.get('x', 1)),
        yoff = uniform(0, bounds.get('y', 1)))
    # rotate
    pgon = affinity.rotate(
        geom = pgon,
        angle  = uniform(0, 360))
    return pgon

def makeTile(points):
    pgon = geometry.Polygon(points)
    centroid = pgon.centroid
    tile = affinity.translate(
        geom = pgon,
        xoff = -centroid.x,
        yoff = -centroid.y)
    return(tile)

class packingSAN(Annealer):

    def __init__(self, state, bounds, tile, scale={}, maxattempts):
        self.bounds = bounds
        self.canvas = geometry.Polygon([(0,0), (0,self.bounds['y']), (self.bounds['x'], self.bounds['y']), (self.bounds['x'], 0)])
        self.tile = tile
        self.scale = scale
        self.maxattempts = maxattempts
        super(packingSAN, self).__init__(state)

    def move(self):
        attempt = 1
        candidate = placeTile(self.tile, self.bounds)
        while not self.canvas.contains(candidate):
            if attempts > self.maxattempts:
                raise Exception(f'Could not place tile within bounds in {maxattempts} attempts. (xbound = {xbound}, ybound = {ybound})')
            candidate = placeTile(self.tile, self.bounds)
            attempt+=1
        self.state = [x for x in self.state if not candidate.overlaps(x)]
        self.state.append(candidate)

    # potential as -1/r. sum combinations for total potential. should make tials attract each other
    def cohesion(self):
        e=0
        for pgon in self.state:
            e += sum([-1/(pgon.centroid.distance(x.centroid)) for x in self.state if x != pgon])
        return(e)

    # potential as d - maxDist where d = distance from origin and diag is the length of the diagonal of the canvas.
    # sum over tials for total potential. should make tials sink into corner
    def sink(self):
        origin = geometry.Point(0,0)
        maxDist = origin.distance(geometry.Point(self.bounds['x'], self.bounds['y']))
        d = sum([origin.distance(x.centroid) - maxDist for x in self.state])
        return(d)

    # potential as -n where n is the number of tials. should increase the number of tials
    def number(self):
        n = len(self.state)
        return(-n)

    # total energy fuction (objective) for a packing
    # ranges from -infinity to 0
    def energy(self):
        e = self.scale.get("cohesion", 1) * self.cohesion() + self.scale.get("sink", 1) * self.sink() + self.scale.get("number", 1) * self.number()
        return(e)
