'output dimensionalities for each column'

import csv
import sys
import re
import math
from collections import defaultdict

def get_words( text ):
	text = text.replace( "'", "" )
	text = re.sub( r'\W+', ' ', text )
	text = text.lower()
	
	text = text.split()
	words = []
	for w in text:
		if w in words:
			continue
		words.append( w )
	return words

###

csv.field_size_limit( 1000000 )

input_file = sys.argv[1]

target_col = 'SalaryNormalized'
cols2tokenize = [ 'Title', 'FullDescription' ]
cols2binarize = [ 'Loc1', 'Loc2', 'Loc3', 'Loc4', 'ContractType', 'ContractTime', 'Company', 'Category', 'SourceName' ]
cols2drop = [  'SalaryRaw' ]

###

i_f = open( input_file )

reader = csv.reader( i_f )
headers = reader.next()

target_index = headers.index( target_col )
indexes2tokenize = map( lambda x: headers.index( x ), cols2tokenize )
indexes2binarize = map( lambda x: headers.index( x ), cols2binarize )
indexes2drop = map( lambda x: headers.index( x ), cols2drop )


n = 0

unique_values = defaultdict( set )

for line in reader:
	for i in indexes2binarize:
		value = line[i]
		unique_values[i].add( value )
	for i in indexes2tokenize:
		words = get_words( line[i] )
		unique_values[i].update( words )
		
	n += 1
	if n % 10000 == 0:
		print n
	
# print counts

for i in sorted( unique_values ):
	l = len( unique_values[i] )
	print "index: %s, count: %s" % ( i, l )
	if l < 100:
		pass
		# print unique_values[i]
		


		
	


		
		
		
		
		
		
		