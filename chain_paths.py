#!/usr/bin/env python
#
# Inkscape extension making long continuous paths from shorter pieces.
# (C) 2015 juewei@fabfolk.com
#
# code snippets visited to learn the extension 'effect' interface:
# - convert2dashes.py
# - http://github.com/jnweiger/inkscape-silhouette
# - http://github.com/jnweiger/inkscape-gears-dev
# - http://sourceforge.net/projects/inkcut/
# - http://code.google.com/p/inkscape2tikz/
# - http://code.google.com/p/eggbotcode/
#
# 2015-11-15 jw, V0.1 -- initial draught

__version__ = '0.1'	# Keep in sync with chain_paths.inx ca line 12
__author__ = 'Juergen Weigert <juewei@fabfolk.com>'

import sys, os, shutil, time, logging, tempfile

# local library
import inkex
import cubicsuperpath
import bezmisc
import simplestyle

inkex.localize()

from optparse import SUPPRESS_HELP

class ChainPaths(inkex.Effect):
  """
  Inkscape Extension make long continuous paths from smaller parts
  """
  def __init__(self):
    # Call the base class constructor.
    inkex.Effect.__init__(self)

    # For handling an SVG viewbox attribute, we will need to know the
    # values of the document's <svg> width and height attributes as well
    # as establishing a transform from the viewbox to the display.
    self.chain_epsilon = 0.01

    self.dumpname= os.path.join(tempfile.gettempdir(), "chain_paths.dump")

    try:
      self.tty = open("/dev/tty", 'w')
    except:
      self.tty = open(os.devnull, 'w')  # '/dev/null' for POSIX, 'nul' for Windows.
    print >>self.tty, "__init__"

    self.OptionParser.add_option('-V', '--version',
          action = 'store_const', const=True, dest = 'version', default = False,
          help='Just print version number ("'+__version__+'") and exit.')
    self.OptionParser.add_option('-s', '--snap', action = 'store', dest = 'snap', type = 'inkbool', default = False, help='snap end-points together when connecting')
    self.OptionParser.add_option('-e', '--epsilon', action = 'store',
          type = 'float', dest = 'chain_epsilon', default = 0.01, help="Max. distance to connect [mm]")

  def version(self):
    return __version__
  def author(self):
    return __author__


  def effect(self):
    if self.options.version:
      print __version__
      sys.exit(0)
    for id, node in self.selected.iteritems():
      if node.tag != inkex.addNS('path','svg'):
        inkex.errormsg(_("Object "+id+" is not a path. Try\n  - Path->Object to Path\n  - Object->Ungroup\n\n------------------------\n"))
      print >>self.tty, "id="+str(id), "tag="+str(node.tag)
      path_d = cubicsuperpath.parsePath(node.get('d'))
      path_style = simplestyle.parseStyle(node.get('style'))
      new = []
      for sub in path_d:
        print >>self.tty, "   sub="+str(sub)
      node.set('style', simplestyle.formatStyle(path_style))
      if node.get(inkex.addNS('type','sodipodi')):
        del node.attrib[inkex.addNS('type', 'sodipodi')]

if __name__ == '__main__':
        e = ChainPaths()

        e.affect()
        sys.exit(0)    # helps to keep the selection
