import sys
import os
import unittest
from pepreader.pep import *
import re

class TestPep( unittest.TestCase ):

    def setUp( self ):
        self.pep = PEP('./tests/fixtures/example.pep')

    def test_parse_file( self ):

        self.assertTrue( type( self.pep.parse_file() ) is list )

    def test_is_header( self ):

        self.assertTrue( self.pep.is_header( '>test' ) )

    def test_is_sequence_empty( self ):

        self.assertTrue( self.pep.is_sequence_empty( None ) )


    def test_append_sequence( self ):

        self.assertEqual( len( self.pep.append_sequence( sequence=None, string='test' ) ), 4 )
        self.assertEqual( len( self.pep.append_sequence( sequence='test', string='test' ) ), 8 )

    def test_all_the_entries_are_there( self ):

        headers = []
        headers_from_pEP = []
        data_from_pep = []

        header = re.compile('(^>.*)')

        with open('./tests/fixtures/example.pep') as f:
            for line in f:

                result = header.search( line )

                if result:
                    result = result.group(0)
                    headers.append( result.rstrip('\r\n') )

        data_from_pep = self.pep.parse_file()

        for data in data_from_pep:
            headers_from_pEP.append( data['header'] )

        count_errors = 0
        for header in headers:
            if not header in headers_from_pEP:
                count_errors = count_errors + 1
                print( header )

        self.assertEqual( count_errors, 0 )

    # That's not garantee all the file was read correctly.
    # But it gives a clue that all the entries of the file was read. 
    def test_if_the_last_line_of_the_file_match_last_sequence( self ):

        data_from_pep = []

        re_header = re.compile('^>')

        with open('./tests/fixtures/example.pep') as f:
            for last_line in f:
                if re_header.search(last_line):
                    header = last_line.rstrip('\r\n')

        last_line = last_line.rstrip('\r\n')

        data_from_pep = self.pep.parse_file()

        for last_data in data_from_pep:
            pass

        last_sequence = last_data['sequence']
        last_header   = last_data['header']

        last_line_size = len( last_line ) 

        if last_sequence[-last_line_size:] == last_line:
            difference = False
        else:
            difference = True


        if header == last_header:
            difference = False
        else:
            difference = True

        self.assertFalse( difference )

    def test_dictionary_keys( self ):

        data_from_pep = []

        data_from_pep = self.pep.parse_file()

        for a_single_record in data_from_pep:
            break

        expected_keys = [ 'header', 'sequence' ]

        read_keys = a_single_record.keys() 

        if len(set(expected_keys) - set(read_keys)) > 0 or len(set(read_keys) - set(expected_keys)) > 0:
            keys_changed = True
        else:
            keys_changed = False

        self.assertFalse( keys_changed )


    def test_get_entry_record( self ):

        positions = self.pep.get_entries_position()

        for position in positions:
            self.assertEqual( type( self.pep.get_entry_record( position ) ) is dict )
            break

    def test_total_of_entries_matches_method_result( self ):

        total_of_entries_from_method  = [] 


        self.pep.generate_entries_position()

        positions = self.pep.get_entries_position()

        for position in positions:
            total_of_entries_from_method.append( self.pep.get_entry_record( position ) )

        total_of_entries_from_method = len(total_of_entries_from_method )


        total_of_entries_from_raw_search = []

        f = open('./tests/fixtures/example.pep')

        re_header = re.compile('^>')

        for line in f:

            result = re_header.search( line )

            if result:
                total_of_entries_from_raw_search.append( line )


        f.seek(0)
        f.close()

        total_of_entries_from_raw_search = len(total_of_entries_from_raw_search)

        self.assertTrue( total_of_entries_from_method == total_of_entries_from_raw_search )

    def test_get_entries_position( self ):

        self.pep.entries_position = []
        self.pep.generate_entries_position()

        positions = self.pep.get_entries_position()

        total_positions_from_method = len(positions)

        total_of_entries_from_raw_search = []

        f = open('./tests/fixtures/example.pep')

        re_header = re.compile('^>')

        for line in f:

            result = re_header.search( line )

            if result:
                total_of_entries_from_raw_search.append( line )


        f.close()

        total_of_entries_from_raw_search = len(total_of_entries_from_raw_search)

        self.assertTrue( total_positions_from_method == total_of_entries_from_raw_search )


if __name__ == "__main__":
    unittest.main()
