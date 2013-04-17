'compute MAE from VW validation and predictions file'
'classification version - map predictions and test values back to salaries'

import sys, csv, math
import numpy as np

#

min_salary = 8.5
max_salary = 12.0 

a_range = np.arange( min_salary, max_salary + 0.1, 0.1 )	# hardcoded min & max
reverse_class_mapping = {}
for i, n in enumerate( a_range ):
	reverse_class_mapping[i+1] = round(n,1)
	
#

test_file = sys.argv[1]
predictions_file = sys.argv[2]

test_reader = csv.reader( open( test_file ), delimiter = " " )
p_reader = csv.reader( open( predictions_file ), delimiter = "\n" )

diffs = []
n = 0

for p_line in p_reader:
	test_line = test_reader.next()
	n += 1
	
	cp = round( float( p_line[0] ), 1 )
	p = reverse_class_mapping[cp]
	p = math.exp( p )
	
	cy = round( float( test_line[0] ), 1 )
	y = reverse_class_mapping[cy]
	y = math.exp( y )

	diffs.append( abs( y - p ))

diffs = sum( diffs )
MAE = diffs / n

print "MAE: %s" % ( MAE )
print