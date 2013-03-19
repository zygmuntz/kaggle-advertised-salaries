'convert a train+test file to libsvm format, using only the features selected by vw-varinfo'

import csv
import sys
import re
import math
from collections import defaultdict
from utils import load_features, get_words, get_token

def construct_libsvm_line( line ):

	global target_index, value_indexes, headers, indexes2binarize, indexes2tokenize, indexes2filter

	label = target_index
	
	new_line = []
	for i in sorted( indexes2binarize + indexes2tokenize ):
	
		col_name = headers[i]
	
		if i in indexes2binarize:
			value = line[i]	
			try:			
				value_index = value_indexes[i][value]
			except KeyError:
				continue
				
			new_item = "%s:1" % ( value_index )
			new_line.append( new_item )
		else:
			text = line[i]
			words = get_words( text )
			
			
			# word_indexes = map( lambda x: value_indexes[i][x], words )
			word_indexes = get_word_indexes( words, i )
			for word_index in sorted( word_indexes ):
				new_item = "%s:1" % ( word_index )
				new_line.append( new_item )		
			
	new_line.insert( 0, label )
	new_line = " ".join( new_line )
	return new_line

	
def get_word_indexes( words, i ):
	global value_indexes
	
	indexes = []
	for word in words:
		try:
			index = value_indexes[i][word]
			indexes.append( index )
		except KeyError:
			pass
	return indexes
	
def pass_filter( value, col_name ):
	global features_by_col

	token = get_token( value )
	if token in features_by_col[col_name]:
		return True
		
def filter_words( words, col_name ):
	filtered_words = []
	for word in words:
		if word in features_by_col[col_name]:
			filtered_words.append( word )
	return filtered_words
	

#################################################

csv.field_size_limit( 1000000 )

features_file = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

target_col = 'SalaryNormalized'
cols2tokenize = [ 'Title', 'FullDescription' ]
cols2binarize = [ 'Loc1', 'Loc2', 'Loc3', 'Loc4', 'Loc5', 'ContractType', 'ContractTime', 'Company', 'Category', 'SourceName' ]
cols2drop = [  'SalaryRaw' ]

# only some features from these columns
cols2filter = [ 'Title', 'FullDescription', 'FullDescription' ]

###

print "loading features..."
features_by_col = load_features( features_file )

print "%s ---> %s" % ( input_file, output_file )

i_f = open( input_file )
o_f = open( output_file, 'wb' )

reader = csv.reader( i_f )
headers = reader.next()

target_index = headers.index( target_col )
indexes2tokenize = map( lambda x: headers.index( x ), cols2tokenize )
indexes2binarize = map( lambda x: headers.index( x ), cols2binarize )
indexes2drop = map( lambda x: headers.index( x ), cols2drop )
indexes2filter = map( lambda x: headers.index( x ), cols2filter )


# first pass: unique values

unique_values = defaultdict( set )

n = 0
for line in reader:
	for i in indexes2binarize:
		value = line[i]
		if pass_filter( value, headers[i] ):
			unique_values[i].add( value )
	
	# the same, but first get unique words from the column text
	# could also use non-unique words, as unique_values[i] is a set
	# using approach no2
	
	for i in indexes2tokenize:
		text = line[i]
		words = get_words( text )
		# filter
		words = filter_words( words, headers[i] )
		for w in words:
			unique_values[i].add( w )
			
	n += 1
	if n % 10000 == 0:
		print n	
	

for i in unique_values:
	print "%s: %s" % ( i, len( unique_values[i] ))
	
# calculate column offsets

offsets = {}		
first_available_offset = 0
for i in sorted( indexes2binarize + indexes2tokenize ):
	offsets[i] = first_available_offset
	first_available_offset += len( unique_values[i] )

# print sorted( offsets.values())

	
# map values to indexes

value_indexes = defaultdict( dict )

for i in unique_values:
	offset = offsets[i]
	for index, value in enumerate( sorted( list( unique_values[i] ))):
		value_indexes[i][value] = offset + index + 1
		
###

print "second pass..."

i_f.seek( 0 )
reader.next()
n = 0

for line in reader:

	new_line = construct_libsvm_line( line )
	o_f.write( new_line + "\n" )
		
	n += 1
	if n % 10000 == 0:
		print n
		
	


		
		
		
		
		
		
		