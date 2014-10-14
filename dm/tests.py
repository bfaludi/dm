
# -*- coding: utf-8 -*-

"""
DM is a Python tool for dict 2 data mapping automatization.
Copyright (C) 2013, Bence Faludi (b.faludi@mito.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

import unittest
from dm import Mapper

class TestObject( object ):
    def __init__( self, **kwarg ):
        for k,v in kwarg.items():
            setattr( self, k, v )

class Test_None( unittest.TestCase ):

    def setUp( self ):

        self.dm = Mapper(None)

    def test_normal( self ):

        self.assertIsNone( self.dm['nothing/thing'] )

class Test_String( unittest.TestCase ):

    def setUp( self ):

        self.dm = Mapper('anything')

    def test_first_char( self ):

        self.assertEqual( self.dm['0'], 'a' )

    def test_last_char( self ):

        self.assertEqual( self.dm['-1'], 'g' )

    def test_char_range( self ):
        
        self.assertEqual( self.dm['0:3'], 'any' )

    def test_not_existing_char( self ):
        
        self.assertEqual( self.dm['32'], None )

class Test_List( unittest.TestCase ):

    def setUp( self ):

        self.dm = Mapper(['first-item','middle','last-item'])

    def test_first( self ):

        self.assertEqual( self.dm['0'], 'first-item' )

    def test_last( self ):

        self.assertEqual( self.dm['-1'], 'last-item' )

    def test_range( self ):
        
        self.assertEqual( self.dm['0:-1'], ['first-item','middle'] )

    def test_not_existing( self ):
        
        self.assertEqual( self.dm['4'], None )

class Test_List_Of_Dictionary( unittest.TestCase ):

    def setUp( self ):

        self.dm = Mapper([
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

        self.dict_dm = Mapper({
            'id': 1,
            'name': 'Steve',
            'others': { 
                'age': 41,
                'childs': { 'year': 1991 }
            },
        })

    def test_slash( self ):

        self.assertEqual( self.dm['~0/id'], 1 )
        self.assertEqual( self.dm['0/id'], 1 )

        self.assertEqual( self.dict_dm['~0/id'], 1 )
        self.assertIsNone( self.dict_dm['0/id'] )

    def test_wo_iteration( self ):

        self.assertIsNone( self.dm['id'] )
        self.assertIsNone( self.dm['name'] )
        self.assertIsNone( self.dm['others/age'] )

    def test_iteration_with_star( self ):

        self.assertEqual( self.dm['*/id'], [1,2,3] )
        self.assertEqual( self.dm['*/name'], ['Steve','Peter','Bruce'] )
        self.assertEqual( self.dm['*/others/age'], [41,31,45] )
        self.assertEqual( self.dm['*/others/childs/*/year'], [None, [1999, 1992], [1987, 1987]] )

    def test_iteration_with_range( self ):

        self.assertEqual( self.dm['0:-1/id'], [1,2] )
        self.assertEqual( self.dm['1:/others/childs/*/year'], [[1999, 1992], [1987, 1987]] )

    def test_with_iteration_and_list_converter( self ):

        self.assertEqual( self.dm['*/others/childs/!/*/year'], [[1991], [1999, 1992], [1987, 1987]] )

    def test_attribute_filter( self ):

        self.assertEqual( self.dm['id=2/name'], 'Peter' )
        self.assertEqual( self.dm['name=Bruce/others/childs/*/year'], [1987, 1987] )

    def test_attribute_iterate_filter( self ):

        self.assertEqual( self.dm['active*=True/name'], ['Steve', 'Bruce'] )

class Test_Dictionary( unittest.TestCase ):

    def setUp( self ):

        self.test_object = TestObject( attr = 'anything' )
        self.dm = Mapper({
            'string': 'item',
            'list': ['first-item','middle','last-item'],
            'object': self.test_object,
            'multi-level': {
                'existing-node': True
            }
        })

    def test_single_level( self ):

        self.assertEqual( self.dm['string'], 'item' )
        self.assertEqual( self.dm['list'], ['first-item','middle','last-item'] )
        self.assertEqual( self.dm['object'], self.test_object )

    def test_multi_level( self ):

        self.assertEqual( self.dm['multi-level/existing-node'], True )
        self.assertEqual( self.dm['multi-level/non-existing-node'], None )

    def test_different_types( self ):

        self.assertEqual( self.dm['list/0'], 'first-item' )
        self.assertEqual( self.dm['object/attr'], 'anything' )
        self.assertEqual( self.dm['string/0:2'], 'it' )

class Test_Object( unittest.TestCase ):

    def setUp( self ):

        self.inner_test_object = TestObject( attr = 'anything' )
        self.test_object = TestObject( 
            string = 'item',
            list = ['first-item','middle','last-item'],
            object = self.inner_test_object
        )
        self.dm = Mapper( self.test_object )

    def test_attribute( self ):

        self.assertEqual( self.dm['string'], 'item' )
        self.assertEqual( self.dm['list'], ['first-item','middle','last-item'] )
        self.assertEqual( self.dm['object'], self.inner_test_object )

    def test_same_types( self ):

        self.assertEqual( self.dm['object/attr'], 'anything' )

    def test_different_types( self ):

        self.assertEqual( self.dm['list/0'], 'first-item' )
        self.assertEqual( self.dm['string/0:2'], 'it' )

class TestRoutes( unittest.TestCase ):

    def setUp( self ):

        self.dm = Mapper({
            'first': {
                'of': {
                    'all': 'with-string',
                    'with': [ 'first-item', 'middle-item', 'last-item' ]
                },
                'and': [ (0, 1), (1, 2), (2, 3), (3, 4) ]
            },
            'filtered': [ { 
                'name': 'first', 
                'value': 'good'
            }, {
                'name': 'second',
                'value': 'normal'
            }, {
                'name': 'third',
                'value': 'bad'
            } ],
            'emptylist': {
                'item': 'itemname'
            },
            'notemptylist': [
                { 'item': 'itemname' },
                { 'item': 'seconditemname' }
            ],
            'strvalue': 'many',
            'strlist': [ 'many', 'list', 'item' ],
            'root': 'R',
            u'útvonal': { u'árvíztűrőtükörfórógép': 4 }
        }, routes = { 
            'first_of_list': 'first/of/with/0',
            'last_of_list': 'first/of/with/-1',
            'tuple_last_first': 'first/and/-1/0',
            'not_existing_route': 'first/of/here',
            'root': 'root',
            'existing_route': 'first/of/all',
            'filtered_list': 'filtered/name=second/value',
            'attributes_from_list': 'filtered/*/value',
            'whole_list_with_star': 'filtered/*',
            'whole_list_wo_star': 'filtered',
            'range_of_list': 'filtered/0:-1/value',
            'attribute_from_dict_via_expected_list': 'emptylist/~0/item',
            'attribute_from_list': 'notemptylist/~0/item',
            'string_value': 'strvalue',
            'string_to_list': 'strvalue/!/0',
            'string_to_list_check_length': 'strvalue/!/1',
            'first_attribute_from_list': 'strlist/!/0',
            'next_attribute_from_list': 'strlist/!/1',
            'accent_path': u'útvonal/árvíztűrőtükörfórógép'
        })

    def test_map_with_list( self ):

        self.assertEqual( self.dm.first_of_list, 'first-item' )
        self.assertEqual( self.dm.last_of_list, 'last-item' )
        self.assertEqual( self.dm.tuple_last_first, 3 )
        self.assertIsNone( self.dm.not_existing_route )
        self.assertEqual( self.dm.root, 'R' )
        self.assertEqual( self.dm.existing_route, 'with-string' )
        self.assertEqual( self.dm.filtered_list, 'normal' )
        self.assertEqual( self.dm.range_of_list, ['good','normal'] )
        self.assertEqual( self.dm.attributes_from_list, ['good','normal','bad'] )
        self.assertEqual( self.dm.attribute_from_dict_via_expected_list, 'itemname' )
        self.assertEqual( self.dm.attribute_from_list, 'itemname' )
        self.assertEqual( self.dm.string_value, 'many' )
        self.assertEqual( self.dm.string_to_list, 'many' )
        self.assertIsNone( self.dm.string_to_list_check_length )
        self.assertEqual( self.dm.first_attribute_from_list, 'many' )
        self.assertEqual( self.dm.next_attribute_from_list, 'list' )
        self.assertEqual( self.dm.whole_list_with_star, self.dm.whole_list_wo_star )
        self.assertEqual( self.dm.accent_path, 4 )

    def test_routes( self ):

        self.assertEqual( self.dm.getRoutes(), {
            'first_of_list': 'first-item',
            'last_of_list': 'last-item',
            'tuple_last_first': 3,
            'not_existing_route': None,
            'root': 'R',
            'existing_route': 'with-string',
            'filtered_list': 'normal',
            'range_of_list': ['good','normal'],
            'attributes_from_list': ['good','normal','bad'],
            'attribute_from_dict_via_expected_list': 'itemname',
            'attribute_from_list': 'itemname',
            'string_value': 'many',
            'string_to_list': 'many',
            'string_to_list_check_length': None,
            'first_attribute_from_list': 'many',
            'next_attribute_from_list': 'list',
            'whole_list_with_star': self.dm.whole_list_wo_star,
            'whole_list_wo_star': self.dm.whole_list_with_star,
            'accent_path': 4,
        })

if __name__ == '__main__':
    unittest.main()