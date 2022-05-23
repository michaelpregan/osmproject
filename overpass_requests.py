# Requires Overpy and Pandas to be installed
# latitude, longitude, and search_radius entries must be numbers
# feature must follow the format of "key"="value" from this table: https://wiki.openstreetmap.org/wiki/Map_features
import overpy
import json
import os
import pandas as pd

def get_API_query(latitude,longitude,search_radius,feature):
	# Gets the input from the user and puts it in query format.
	# If more time is neded, increase the number in the timeout brackets.
	query_start = '''[timeout:3600];(nwr['''
	query_middle = '''](around:'''
	boundaries = search_radius+','+latitude+','+longitude
	query_end = '''););out;'''
	user_query = query_start+feature+query_middle+boundaries+query_end
	return(user_query)

def overpass_query(query):
	# Communicates the query with Overpass, collects the data from each element, and exports the data to a csv file.
	api = overpy.Overpass()
	result = api.query(query)
	nodes = []
	for node in result.nodes:
		node.tags['id'] = node.id
		nodes.append(node.tags)
	df = pd.DataFrame(nodes)
	path = os.getcwd()
	os.makedirs('OSM',exist_ok=True)
	df.to_csv(os.path.join(path,'OSM','output.csv'),index=False)
	return(print('Output file generated!'))

user_latitude = input('Latitude: ')
user_longitude = input('Longitude: ')
user_search_radius = input('Radius (enter a whole number, in meters): ')
user_feature = input('''Feature (example: "amenity"="hospital"): ''')
input = get_API_query(user_latitude,user_longitude,user_search_radius,user_feature)
overpass_query(input)
