import logging

# A library must not configure logging for the application that imports it
# (upstream called logging.basicConfig(level=DEBUG) here). Applications and
# scripts configure handlers themselves; without that, records are dropped.
logging.getLogger("idotmatrix").addHandler(logging.NullHandler())
