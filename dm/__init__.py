
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

import copy
from .compat import *

class Mapper( object ):

    """
    This is mapper object for the data.
    """

    # void
    def __init__( self, data, routes = None ):

        """
        This is the constructor of the mapper object.

        @param data: Given data you want to precess
        @type data: type

        @param routes: Given predefined routes to calculate
        @type routes: dict
        """

        self.data = data
        self.routes = routes or {}

    # type
    def __getitem__( self, rule ):

        """
        Returns a value based on your rule's route.

        @param rule: Route
        @type rule: unicode

        @return: Item in the end of the path.
        @rtype: type
        """

        try:
            return self.getDataByRule( text_type( rule ) )

        except IndexError:
            return None

        except KeyError:
            return None

    # type
    def __getattr__( self, route_name ):

        """
        Returns a calculated route.

        @param route_name: Name of the route
        @type route_name: unicode

        @return: Item in the end of the route's path.
        @rtype: type
        """

        if text_type( route_name ) not in iterkeys_(self.routes):
            raise IndexError('Not existing predefined route name')

        return self[ self.routes[ text_type( route_name ) ] ]

    # str
    def __repr__( self ):

        """
        Self representative.
        """

        return '<{}.{} with {}>'.format( 
            self.__class__.__module__, 
            self.__class__.__name__, 
            repr( self.data ) 
        )

    # dict
    def getRoutes( self ):

        """
        Returns all of the route's value.

        @return: All of the route's value.
        @rtype: dict
        """

        return {
            route_name : self[ self.routes[ text_type( route_name ) ] ] \
            for route_name in iterkeys_(self.routes)
        }

    # type
    def getDataByRule( self, rule, current_data = None ):

        """
        Returns the date in the end of the rule's route.

        @param rule: Given rule
        @type rule: unicode

        @param current_data: Given data to iterate.
        @type current_data: type

        @return: Item in the end of the route's path.
        @rtype: type
        """

        # bool
        def is_integer( s ):
            if s[0] in (u'-', u'+'):
                return s[1:].isdigit()

            return s.isdigit()

        current_object = current_data or self.data

        # If there is no rule, return the current data
        if len( rule ) == 0:
            return current_object

        # Iterate over the given rule's route
        for rule_part in rule.split(u'/'):

            # If it starts with a !, then convert into a list
            if rule_part == u'!':
                if not isinstance( current_object, ( list, tuple ) ):
                    current_object = [ current_object ]

                continue

            if isinstance( current_object, dict ): 
                if rule_part in current_object:
                    current_object = current_object[ rule_part ]

                # If it starts with a ~, we ignore the rule part
                elif rule_part[0] == u'~':
                    current_object = current_object

                elif is_integer( rule_part ):
                    current_object = current_object[ int( rule_part ) ]

                else:
                    return None

            elif isinstance( current_object, ( list, tuple ) ):
                rule_continues_idx = rule.index( rule_part ) + len( rule_part ) + 1

                # If it starts with a ~, we use the rule as normal
                if rule_part[0] == u'~':
                    rule_part = rule_part[1:]

                # If it contains a =, we filter out that record
                if rule_part.count(u'*=') == 1:
                    object_name, object_value = rule_part.split(u'*=')
                    new_object = []
                    for item in current_object:
                        if text_type( item[object_name] ) == object_value:
                            new_object.append( self.getDataByRule( 
                                rule[ rule_continues_idx: ],
                                item
                            ))

                    return new_object

                # If it contains a =, we filter out that record
                elif rule_part.count(u'=') == 1 and rule_part.count(u'*') == 0:
                    object_name, object_value = rule_part.split(u'=')
                    for item in current_object:
                        if text_type( item[object_name] ) == object_value:
                            current_object = item
                            continue

                # If its a star, we iterate over the list
                elif rule_part == u'*':
                    new_object = []
                    if len( rule[ rule_continues_idx: ] ) == 0:
                        return current_object
                        
                    for item in current_object:
                        new_object.append( self.getDataByRule( 
                            rule[ rule_continues_idx: ],
                            item
                        ))
                    return new_object

                elif rule_part.count(u':') == 1:
                    pts = rule_part.split(u':')
                    new_object = []
                    pts0 = None if len( pts[0] ) == 0 else int( pts[0] )
                    pts1 = None if len( pts[1] ) == 0 else int( pts[1] )
                    for item in current_object[ pts0 : pts1 ]:
                        new_object.append( self.getDataByRule( 
                            rule[ rule_continues_idx: ],
                            item
                        ))
                    return new_object

                elif is_integer( rule_part ):
                    current_object = current_object[ int( rule_part ) ]

                else:
                    return None

            elif current_object is None:
                return None

            elif isinstance( current_object, object ) and not isinstance( current_object, string_types + integer_types + ( float, bool, ) ):
                current_object = getattr( current_object, rule_part )

            elif isinstance( current_object, string_types ):
                pts = rule_part.split(u':')
                if len( pts ) == 2:
                    pts0 = None if len( pts[0] ) == 0 else int( pts[0] )
                    pts1 = None if len( pts[1] ) == 0 else int( pts[1] )
                    current_object = current_object[ pts0 : pts1 ].strip()

                elif is_integer( rule_part ):
                    current_object = current_object[ int( rule_part ) ]

                else:
                    return None

        return current_object
