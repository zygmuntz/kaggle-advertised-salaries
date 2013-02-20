# convert VW's log predictions back to a normal scale by taking exp()

input_file = 'data/p.txt' 
output_file = 'data/sub.txt' 

p = as.numeric( readLines( input_file ))
p = exp( p )

writeLines( as.character( p ), output_file )
