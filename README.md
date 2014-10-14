
## dm / Data Mapper

Use this tool to map any kind of data to the right place.

	import dm
	
	data = dm.Mapper({
	    'id': 1,
	    'name': 'Steve',
	    'others': { 
	        'age': 41,
	        'childs': { 'year': 1991 }
	    },
	})
	
	print( data['others/age'] )
	# 42
	
	print( data['others/childs/year'] )
	# 1991
	
	print( data['others/notexists'] )
	# None

This package works well for Python **2.x** and **3.x**!

### Overview

Each map means a path to the "data". The path can contain words, numbers (indices) and the combinations of them divided by a `/`.

In the light of this, let's see a more complex example based on which it will be easier to understand the process. The dataset could contain multidimensional lists and could contain one-dimensional information as well.

This package is part of the [mETL](https://github.com/ceumicrodata/mETL) extract, transform, load tool.

#### Installation

Open a terminal and write the following:

	$ easy_install dm

#### Operators

- `/`: Defines a next level in the given path/mapping.
- `*`: Checks all elements in the case of lists.
- `~`: Test operator for list to dict, if both list and dict can exist on the same level. If list exists, it can be defined what we look for, if dict exists, nothing happens, the process goes on in the given path from the next element.
- `!`: Operator that converts data to list. It is used if we want to get a list but it is not known whether we will get that or not.
- `=`: Filter the list's given value

#### Examples

##### Basic

	import dm
	
	data = dm.Mapper({
	    'id': 1,
	    'name': 'Steve',
	    'others': { 
	        'age': 41,
	        'childs': { 'year': 1991 }
	    },
	})
	
	print( data['others/age'] )
	# 42
	
	print( data['others/childs/year'] )
	# 1991
	
	print( data['others/notexists'] )
	# None

##### Iterators & converters

	import dm
	
	data = dm.Mapper([
	    {
	        'id': 1,
	        'active': True,
	        'name': 'Steve',
	        'others': { 
	            'age': 41,
	            'childs': { 'year': 1991 }
	        },
	    },
	    { 
	        'id': 2,
	        'active': False,
	        'name': 'Peter',
	        'others': { 
	            'age': 31,
	            'childs': [{ 'year': 1999 },{ 'year': 1992 }]
	        },
	    },
	    {
	        'id': 3,
	        'active': True,
	        'name': 'Bruce',
	        'others': { 
	            'age': 45,
	            'childs': [{ 'year': 1987 },{ 'year': 1987 }]
	        },
	    }
	])
	
	print( data['*/name'] )
	# ['Steve', 'Peter', 'Bruce']
	
	print( data['*/others/childs/*/year'] )
	# [None, [1999, 1992], [1987, 1987]]
	
	print( data['*/others/childs/!/*/year'] )
	# [[1991], [1999, 1992], [1987, 1987]]
	
	print( data['*/others/childs/!/0/year'] )
	# [1991, 1999, 1987]
	
	print( data['id=2/name'] )
	# 'Peter'

Enjoy!