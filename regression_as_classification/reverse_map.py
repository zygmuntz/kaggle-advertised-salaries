'map predictions from classes to real [regression] values'

import sys, csv
import numpy as np

min_salary = 8.5
max_salary = 12.0 

a_range = np.arange( min_salary, max_salary + 0.1, 0.1 )	# hardcoded min & max
reverse_class_mapping = {}
for i, n in enumerate( a_range ):
	reverse_class_mapping[i+1] = round(n,1)
	
input_file = sys.argv[1]
output_file = sys.argv[2]

i_f = open( input_file )
o_f = open( output_file, 'wb' )

for line in i_f:
	c = round( float( line.strip()), 1 )
	log_salary = reverse_class_mapping[c]
	o_f.write( "%s\n" % log_salary )
	