import dbm
import cPickle as pickle

__database = None

def open(filename):
	print("using "+filename+" as database")
	global __database
	__database = dbm.open(filename, "c")
	
def get(k):
	return pickle.loads(__database[k])

def set(k, v):
	__database[k] = pickle.dumps(v)

def isset(k):
	return k in __database

