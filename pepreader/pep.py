import re
import pprint

class PEP:
    """
    Deals with Fasta file in the *.pep format, typical from KEGG databases released at least until 2015.

    This class opens, parse entries and return formated raw file in a more handy structure.

    Attributes:
        file_to_parse(file): File handle that represents the 'pep' file to parse.
        entries_position(list): List of positions (char position in the file) of every entry.
    """

    def __init__(self, pep_file=None):
    # This class is supposed to parse a single file per moment.
        self.file_to_parse = pep_file
        self.entries_position = []

    def is_header( self, string=None ):
        """
        Test if the string is a typical PEP file header (starts with '>').

        Args:
            string(str): String to be tested.
        """

        re_header = re.compile('^>')
        re_header_result = re_header.search( string )

        if re_header_result:
            return True
        else:
            return False


    def is_sequence_empty( self, sequence=None ):
        """
        Test if the list of sequences is empty.

        Args:
            sequence(list): The list of sequences.
        """

        if sequence == None:
            return True 
        else:
            return False 


    def append_sequence( self, sequence=None, string=None ):
        """
        Generates the full sequence by appending parts of sequence in its previous part.

        Args:
            sequence(str): Previous part of the sequence.
            string(str): Part of sequence to be appended.

        Returns:
            (str): Concatenated string.
        """

        # Means the first time, in other words, at the first time 'sequence' (the previous) will be None and string
        # actual has something.
        if sequence == None:
            result = string
        else:
            result = sequence + string

        return result 


    def parse_file( self ):
        """
        Return a list of dictionaries.

        Each dictionary is a entry from the PEP file.

        Each dictionary entry has a 'header' and a 'sequence' key.

        Returns:
            (list): [ {'header': header, 'sequence': sequence } ]
        """

        # Flags
        found_header = False
        read_content = True

        # The sequence
        sequence = None

        # Our result
        proteins= []

        with open(self.file_to_parse) as pep:
            with pep as pep_file:
                for line in pep_file:
                    # The line is a header (starts with '>')
                    # This conditional has a important role: indicate when to insert the entry in the 'proteins' list.
                    if self.is_header( line ):

                        # If we're in a header line and also if there's sequences already read, it means there's a entire 
                        # entry already read that has to be put in the 'proteins' list.
                        if not self.is_sequence_empty( sequence ):
                            proteins.append( { 'header': header, 'sequence': sequence } )

                            # Reset sequence
                            sequence = None

                        # We have to keep the header line for later insertion.
                        header = line.rstrip('\r\n')

                    # So, the line is not a header, in other words, that's a ordinary sequence line.
                    else:
                        sequence = self.append_sequence( sequence, line.rstrip('\r\n') )
                        

        # This part of the code deals exclusively with the last entry from the pep file.
        # It means, when we finished the loop above, still there's the read entry that wasn't mark
        # to be inserted because there's not a header line (after the end of the file, of course) to indicate the entry has to be inserted.
        if not self.is_sequence_empty( sequence ):
            proteins.append( {'header': header, 'sequence': sequence } )

        if not pep_file.closed:
            pep_file.close()

        return proteins

    def get_entry_record( self, offset=None ):
        """
        Return entries in a dictionary format.

        This method is supposed to be executed in a assisted way, in other words, immediately returns an Fasta entry as soon as it finished an entry reading.

        This method is supposed to be called after a setup that includes:
        
        * open a file handle
        * set it to the class (self.set_file)
        * generate all the entries position of the file (self.generate_entries_position)
        * get the entries position (self.get_entries_position)
        * and be called inside a loop through those entry positions (which are the 'offset' parameter').

        Example:

            pep = PEP()
            f = open( '../tests/fixtures/example.pep' )

            pep.set_file( f ) 
            pep.generate_entries_position()
            positions = pep.get_entries_position()

            for position in positions:
                result = pep.get_entry_record( position )


        Args:
            offset(int): The position of the file (the file handle) to start reading entries.

        Returns:
            (dict): a dictionary with the header and sequence with the entry. 
        """
        # Flags
        found_header = False
        read_content = True

        # The sequence
        sequence = None

        # Our result
        protein = {} 

        with open(self.file_to_parse) as pep:
            pep.seek( offset )

            for line in pep:
                # The line is a header (starts with '>')
                # This conditional has a important role: indicate when to fill 'protein' dictionary.
                if self.is_header( line ):

                    header_size = len( line )

                    # If we're in a header line and also if there's sequences already read, it means there's a entire 
                    # entry already read that has to be put in the 'protein' dictionary.
                    if not self.is_sequence_empty( sequence ):
                        protein['header']   = header
                        protein['sequence'] = sequence

                        # Reset sequence
                        sequence = None

                        return protein 

                    # We have to keep the header line for later insertion.
                    header = line.rstrip('\r\n')

                # So, the line is not a header, in other words, that's a ordinary sequence line.
                else:
                    sequence = self.append_sequence( sequence, line.rstrip('\r\n') )

            # Weird, but the line below means the entry that remains at the end of the file.
            # That happens because the code above consider a header line as a trigger to store the previous entry.
            # Since the code reach the end of the file, there's no next header to trigger the entry that was right read.
            # So the line below stores what was read but not triggeded to be stored.
            protein['header']   = header
            protein['sequence'] = sequence

        return protein 


    def generate_entries_position( self ):
        """
        Generates a list with the start position of every entry of the Fasta pep file.

        Returns:
            (void): Fill the class property entries_position. 
        """

        # Reset any previous value.
        self.entries_position = []

        # First header have to be ignored since that's where we start reading an entry.
        first_header = True

        # First position, of course, is zero.
        position = 0

        # We add zero as our first position.
        self.entries_position.append( 0 )

        # Walk through the file.
        with open(self.file_to_parse) as opened_pep_file:
            for line in opened_pep_file:

                # New position is the previous position plus the line size, plus 1 (that '1' means the beginning of the next entry).
                position = position + len(line.rstrip('\r\n')) + 1

                # If the line is a header and it's not the first header.
                if self.is_header( line ) and first_header == False:
                    # Get the size of the header.
                    header_size = len( line )

                    # New position entry is the current position minus the size of the current header (means back to the beginning of the line).
                    position = position - header_size 

                    # We have to keep the header position. That's for the last entry of the whole file. That's becaus Fasta files doesn't have any END entry mark,
                    # so, our last entry is marked by the end of the file itself, which means we already finished this loop when we should read the entry position, what
                    # makes impossible to execute the loop 'append'.
                    header_position = position

                    # Add the new position.
                    self.entries_position.append( position )

                    # Put back the whole line size (since we have to keep reading the next entries from the last entire line).
                    position = position + header_size

                # Tell we're not at the first header anymore.
                if first_header == True:
                    first_header = False

        
    def get_entries_position( self ):
        """
        Returns the entry position of all the entries in the Fasta pep file.

        Returns:
            (list): All the entry positions from the Fasta pep file.
        """

        return self.entries_position





