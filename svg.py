from svgpathtools import Line, Path, svg2paths2, wsvg
from shapely import geometry, affinity

# translate tile such that it's centroid is at the origin
def centerTile(tile):
    centroid = tile.centroid
    newTile = affinity.translate(
        geom = tile,
        xoff = -centroid.x,
        yoff = -centroid.y)
    return(newTile)

# convert scgpathtools.Path to shapely.goemetry.Polygon
def pathToPolygon(path):
    points = [(x.start.real, x.start.imag) for x in path]
    tile = geometry.Polygon(points)
    return(tile)

# convert shapely.goemetry.Polygon to svgpathtools.Path
def polygonToPath(pgon):
    wkt = pgon.to_wkt()
    stripped = wkt[10:-3]       # strip "POLYGON ((" from front and "))" from end
    pairs = [s.split(' ') for s in stripped.split(', ')]
    start_points = [complex(float(p[0]), float(p[1])) for p in pairs]
    end_points = start_points[1:]
    end_points.append(start_points[0])
    lines = []
    for i in range(0, len(start_points)):
        lines.append(Line(start = start_points[i], end = end_points[i]))
    path = Path()
    for line in lines:
        path.append(line)
    return(path)

# create a tile object from a vector graphics file
def readTileFromSVG(fname):
    paths, attributes, svg_attributes = svg2paths2(fname)
    tile = geometry.Polygon()
    for path in paths:
        points = [(x.start.real, x.start.imag) for x in path]
        tile = tile.union(geometry.Polygon(points))
    tile = centerTile(tile)
    return(tile)

# save packing as svg file
def writePackingToSVG(filename, packing):
    paths = [polygonToPath(tile) for tile in packing]
    wsvg(paths, filename=filename)
