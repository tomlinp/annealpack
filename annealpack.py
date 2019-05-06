import click
import pickle
import sys

import annealing
import svg

@click.command(context_settings={"ignore_unknown_options": True})
@click.option('-x', '--xbound', default=10.0, type=float, help="Size of canvas in x-dimension.  Defaults to 10.")
@click.option('-y', '--ybound', default=10.0, type=float, help="Size of canvas in y-dimension.  Defaults to 10.")
@click.option('--continue', 'load_initial', default=False, is_flag=True, help="Continue from a saved state.  Useful for chaining optimizations.")
@click.option('--maxattempts', default=10000, type=int, help="Number of times to try placing a tile before giving up")
@click.option('--save', default='', type=str, help="Optional file to save output state to.")
@click.option('--scale', nargs=3, default=(1.0, 1.0, 1.0), type=float, help="The 3 scaling parameters for the cohesion, sink, and number (in that order) parts of the energy function.  All scaling parameters default to 1.")
@click.option('--tmax', default=25000.0, type=float, help="Max (starting) temperature of annealer")
@click.option('--tmin', default=2.5, type=float, help="Min (ending) temperature of annealer")
@click.option('--steps', default=50000, type=int, help="Number of iterations for annealer")
@click.option('--updates', default=100, type=int, help="Number of updates for annealer (by default an update prints to stdout)")
@click.argument('infile', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path())
def cli(infile, outfile, xbound, ybound, load_initial, maxattempts, save, scale, tmax, tmin,steps, updates):
    # Check if we are loading a state, or starting fresh.
    if load_initial:
        try:
            # Read in inital state and tile
            loaded = pickle.load(infile)
            tile = loaded['tile']
            state = loaded['state']
        except:
            click.echo(f'Unable to read initial state from {infile}')
            sys.exit()
    else:
        try:
            # Read in tile
            tile = svg.readTileFromSVG(infile)
            state = []
        except:
            click.echo(f'Unable to read tile from {infile}')
            sys.exit()

    # define canvas bounds and scaleing factors
    bounds = {'x':xbound, 'y':ybound}
    scale = {'coheaseion':scale[0], 'sink':scale[1], 'number':scale[2]}

    # perform simulated annealing
    a = annealing.packingSAN(state, bounds, tile, maxattempts, scale)
    a.Tmax = tmax
    a.Tmin = tmin
    a.steps = steps
    a.updates = updates
    packing, energy = a.anneal()

    # write out result as csv
    svg.writePackingToSVG(outfile, packing)

    # save state if desired
    if save:
        pickle.dump({"tile":tile, "state":packing}, save)

    # carrige return to avoid clobbering terminal output
    click.echo("\n")
