# Requires Overpy and Pandas to be installed
import overpy
import json
import pandas as pd

def get_API_query():
	# Gets the input from the user. 
	# Latitude, longitude, and search radius entries must only be numbers
	# Parameter must follow the format "Key"="Value" from this table: https://wiki.openstreetmap.org/wiki/Map_features
	print('Latitude:')
	latitude = input()
	print('Longitude:')
	longitude = input()
	print('Search Radius (in meters):')
	radius = input()
	print('''What are you looking for? (example:"amenity"="hospital")''')
	parameter = input()

	# Puts the input in query format. If more time is neded, increase the number in the timeout brackets.
	query_start = '''[timeout:3600];(nwr['''
	query_middle = '''](around:'''
	user_boundaries = radius+','+latitude+','+longitude
	query_end = '''););out;'''
	query = query_start+parameter+query_middle+user_boundaries+query_end
	return(query)

def overpass_query(input):
	# Communicates the query with Overpass, collects the data from each element, and exports the data to a csv file.
	api = overpy.Overpass()
	result = api.query(input)
	nodes = []
	for node in result.nodes:
		node.tags['id'] = node.id
		nodes.append(node.tags)
	df = pd.DataFrame(nodes)
	df.to_csv('output.csv',index=False)
	return(print('Output file generated!'))

user_query = get_API_query()
overpass_query(user_query)
