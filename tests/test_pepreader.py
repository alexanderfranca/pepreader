import sys
import os
import unittest
from pepreader.pepreader import *
from pepreader.pep import *
import re


class test_PEPReader( unittest.TestCase ):

    def setUp( self ):

        pep = PEP('./tests/fixtures/example.pep')
        self.pepr = PEPReader(pep=pep)

    def test_parsed_file( self ):

        self.assertTrue( type( self.pepr.parsed_file() ) is list )

    def test_protein_identification( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'

        self.assertEqual( self.pepr.protein_identification( header ), 'rno:294324'  )

    def test_protein_description( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'

        self.assertEqual( self.pepr.protein_description( header ), 'Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]' )

    def test_has_ec_from_square_brackets( self ):

        header_with_ec='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'
        header_without_ec='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase '

        self.assertTrue( self.pepr.has_ec_from_square_brackets( header_with_ec ) )
        self.assertFalse( self.pepr.has_ec_from_square_brackets( header_without_ec ) )

    def test_has_ec_from_brackets( self ):

        header_with_ec='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3 (EC:2.3.1.51); K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'
        header_without_ec='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3;  K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'

        self.assertTrue( self.pepr.has_ec_from_brackets( header_with_ec ) )
        self.assertFalse( self.pepr.has_ec_from_brackets( header_without_ec ) )

    def test_ec_from_square_brackets( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3; K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase [EC:2.3.1.51 2.3.1.-]'

        self.assertEqual( self.pepr.ec_from_square_brackets( header ), [ '2.3.1.51', '2.3.1.-' ] )

    def test_ec_from_brackets( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3; K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase (EC:2.3.1.51 2.3.1.-) extra string'

        self.assertEqual( self.pepr.ec_from_brackets( header ), [ '2.3.1.51', '2.3.1.-' ] )

    def test_organism_code( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3; K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase (EC:2.3.1.51 2.3.1.-) extra string'

        self.assertEqual( self.pepr.organism_code( header ), 'rno' )

    def test_full_fasta_header( self ):

        header='>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3; K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase (EC:2.3.1.51 2.3.1.-) extra string'

        self.assertEqual( self.pepr.full_fasta_header( header ), '>rno:294324  Agpat3; 1-acylglycerol-3-phosphate O-acyltransferase 3; K13523 lysophosphatidic acid acyltransferase / lysophosphatidylinositol acyltransferase (EC:2.3.1.51 2.3.1.-) extra string' )


    def test_entries_position( self ):

        self.assertTrue( type( self.pepr.entries_position() ) is list )

if __name__ == "__main__":
    unittest.main()
