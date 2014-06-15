'some helper functions'

import re
from collections import defaultdict

def load_features( input_file ):

	i_f = open( input_file )
	# o_f = open( output_file, 'wb' )

	features_by_col = defaultdict( dict )

	for line in i_f:
		line = line.split( ' ', 1 )
		col_feature = line[0]
		try:
			col, feature = col_feature.split( '^' )
		except ValueError:
			print col_feature
			continue
		features_by_col[col][feature] = 1

	print	
	for col in features_by_col:
		print "%s: %s" % ( col, len( features_by_col[col] ))
		
	return features_by_col
	
'for categorical variables'
def get_token( text ):
	text = text.replace( "|", " " )
	text = text.replace( ":", " " )
	text = text.replace( " ", "_" )
	return text	
	
def get_words( text ):
	text = get_sequence_of_words( text )
	text = text.split()
	
	words = []
	for w in text:
		if w in words:
			continue
		words.append( w )
		
	return words	
	
"like get_words(), but don't filter out unique and retain sequence"	
def get_sequence_of_words( text ):
	text = text.replace( "'", "" )
	text = re.sub( r'\W+', ' ', text )
	text = text.lower()
	
	return text