'add dummy salaries columns (2) to a test file; drop headers'

import csv
import sys

csv.field_size_limit( 1000000 )

input_file = sys.argv[1]
output_file = sys.argv[2]

i_f = open( input_file )
o_f = open( output_file, 'wb' )

reader = csv.reader( i_f )
writer = csv.writer( o_f )

headers = reader.next()

target_index = 9

for line in reader:
	line.insert( target_index, '1' )
	line.insert( target_index, '1' )
	writer.writerow( line )
		

	


		
		
		
		
		
		
		