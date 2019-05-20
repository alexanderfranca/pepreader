# -*- coding: utf-8 -*-

# Import essential modules
from pepreader.pepreader import PEPReader 
from pepreader.pep import PEP 

# Load the reader and load the dbgetreader
pep = PEP(pep_file='./tests/fixtures/example.pep')
pepreader = PEPReader(pep=pep)

# Get the positions from all the entries from the chosen file
positions = pepreader.entries_position()

# Iterate through all the positions and get the entry for that position.
for position in positions:
    entry = pepreader.parsed_entry(position)
    print(entry['identification'])
