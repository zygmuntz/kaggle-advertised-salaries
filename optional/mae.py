'compute MAE from VW validation and predictions file'

import sys, csv, math

test_file = sys.argv[1]
predictions_file = sys.argv[2]

test_reader = csv.reader( open( test_file ), delimiter = " " )
p_reader = csv.reader( open( predictions_file ), delimiter = "\n" )

diffs = []
n = 0

for p_line in p_reader:
	test_line = test_reader.next()
	n += 1
	
	p = math.exp( float( p_line[0] ))
	y = math.exp( float( test_line[0] ))

	diffs.append( abs( y - p ))

diffs = sum( diffs )
MAE = diffs / n

print "MAE: %s" % ( MAE )
print