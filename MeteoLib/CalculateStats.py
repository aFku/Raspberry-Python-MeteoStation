def calculate_average(iterable_data, pos=None):
	"""
	Calculate average of given iterable element
	pos can be int and it is index when given iterable contain iterable with data to calculation under pos.
	"""
	if pos:
		return sum([data[pos] for data in iterable_data]) / len(iterable_data)
	else:
		return sum(iterable_data) / len(iterable_data)


def narrow_data_range(namedtuple_list, start, end):
	"""
	Extract namedtuple from list and return given range of data 
	"""
	return [data for data in namedtuple_list if data.date > start and data.date < end]



