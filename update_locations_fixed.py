'replace location columns from the original file with parsed location (five columns)'
'update_locations.py Location_Tree.csv input.csv output.csv'

import sys, csv
from collections import defaultdict
from pprint import pprint

###

def get_full_loc( loc ):
	global levels

	full_loc = [ loc ]

	for l in range( 5, -1, -1 ):
		try:
			parent = levels[l][loc]
			if parent is None:
				break
			full_loc.insert( 0, parent )
			loc = parent
		except KeyError:
			continue
		
	# failsafe
	if full_loc[0] != 'UK':
		full_loc = [ '' ] * 5
		full_loc[0] = 'UK'
		full_loc[1] = loc	
	else:
		full_loc = full_loc + [ '', '', '', '', '' ]
		full_loc = full_loc[:5]
	
	return full_loc

###

loc_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

# loc_file = 'data/orig/Location_Tree.csv'
loc_col = 'LocationNormalized'

l_f = open( loc_file )
reader = csv.reader( l_f, delimiter = '"' )

# first pass: build a dictionary

levels = defaultdict( dict )

for line in reader:
	line = line[0].split( '~' )
	parent = None
	for i, loc in enumerate( line ):
		levels[i][loc] = parent
		parent = loc
		
del levels[6]
print "levels: %s" % ( sorted( levels.keys()))
		
# second pass: update data

i_f = open( input_file )
o_f = open( output_file, 'wb' )

reader = csv.reader( i_f )
writer = csv.writer( o_f )


# headers

headers = reader.next()
loc_col_i = headers.index( loc_col )

full_loc_headers = [ 'Loc1', 'Loc2', 'Loc3', 'Loc4', 'Loc5' ]
headers = headers[0:loc_col_i - 1] + full_loc_headers + headers[loc_col_i + 1:]

writer.writerow( headers )

n = 0
for line in reader:
	loc = line[loc_col_i]
	full_loc = get_full_loc( loc )
	
	# getting rid of loc description
	new_line = line[0:loc_col_i - 1] + full_loc + line[loc_col_i + 1:]
	writer.writerow( new_line )
	
	n += 1
	if n % 10000 == 0:
		print n
		