'convert a train+test file to VW format. Locations in Loc1...Loc5.'

import csv
import sys
import re
import math
from collections import defaultdict

def construct_vw_line( line, value_indexes, headers ):
	label = line[target_index]
	label = str( math.log( float( label )))
	
	new_line = []
	
	for i in indexes2tokenize:
		col_name = headers[i]
		words = get_words( line[i] )
		new_item = "|%s %s" % ( col_name, words )
		new_line.append( new_item )
		
	for i in indexes2binarize:
		col_name = headers[i]
		value = line[i]
		value_index = value_indexes[i][value]
		new_item = "|%s %s" % ( col_name, value_index )	
		new_line.append( new_item )
	
	new_line.insert( 0, label )
	new_line = " ".join( new_line )
	return new_line
	
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
		
	words = " ".join( words )
	return words	

#################################################


csv.field_size_limit( 1000000 )

input_file = sys.argv[1]
output_file = sys.argv[2]

target_col = 'SalaryNormalized'
cols2tokenize = [ 'Title', 'FullDescription' ]
cols2binarize = [ 'Loc1', 'Loc2', 'Loc3', 'Loc4', 'Loc5', 'ContractType', 'ContractTime', 'Company', 'Category', 'SourceName' ]
cols2drop = [  'SalaryRaw' ]

###

print "%s ---> %s" % ( input_file, output_file )

i_f = open( input_file )
o_f = open( output_file, 'wb' )

reader = csv.reader( i_f )
headers = reader.next()

target_index = headers.index( target_col )
indexes2tokenize = map( lambda x: headers.index( x ), cols2tokenize )
indexes2binarize = map( lambda x: headers.index( x ), cols2binarize )
indexes2drop = map( lambda x: headers.index( x ), cols2drop )
#print indexes2binarize

# first pass: unique values

unique_values = defaultdict( set )

for line in reader:
	for i in indexes2binarize:
		value = line[i]
		unique_values[i].add( value )
		
	
# mapping values to indexes

value_indexes = defaultdict( dict )

for i in unique_values:
	for index, value in enumerate( sorted( list( unique_values[i] ))):
		value_indexes[i][value] = index + 1
		

print "second pass..."

i_f.seek( 0 )
reader.next()
n = 0

for line in reader:

	new_line = construct_vw_line( line, value_indexes, headers )
	o_f.write( new_line + "\n" )
		
	n += 1
	if n % 10000 == 0:
		print n
		
	


		
		
		
		
		
		
		