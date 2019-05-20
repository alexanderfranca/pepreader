import re
import pprint

class PEPReader:
    """
    Read 'pep' files and return entries in a dict format.

    Attributes:
        pep(class): PEP class.
        file_to_parse(file): File handle that represents the 'pep' file to read.
        entries_position(list): List of entries position (char position in the file) of every entry.
    """

    def __init__( self, pep ):
        self.pep = pep 

        self.file_to_parse = None
        self.pep_entries_position = []

    def parsed_file( self ):
        """
        Returns list of pep (Fasta) headers and its sequences.
        """

        pep_data = self.pep.parse_file()

        return pep_data

    def entries_position( self ):
        """
        Returns the entries position of the pep file.

        Returns:
            (list): Entries position (numbers) of the entries in the *pep file.
        """

        self.pep.generate_entries_position()
        positions = self.pep.entries_position

        return positions


    def parsed_entry( self, offset=None ):
        """
        Returns the entry of a pep file in a dictionary format.

        Args:
            offset(int): Position inside the file handle.

        Returns:
            (dict): Dictionary containing an pep file entry.
        """

        pep_entry = self.pep.get_entry_record( offset )

        protein = {}

        protein['identification'] = self.protein_identification( pep_entry['header'] )
        protein['full_fasta_header'] = self.full_fasta_header( pep_entry['header'] )
        protein['description'] = self.protein_description( pep_entry['header'] )
        protein['sequence'] = pep_entry['sequence']

        return protein 

    def protein_identification( self, header=None ):
        """
        Return the protein identification from a Fasta header.

        Args:
            header(str): A Fasta header.

        Returns:
            (str): Protein identification.
        """

        protein_identification = header.split(' ')
        protein_identification = protein_identification[0]
        protein_identification = protein_identification.replace('>','')
        protein_identification = protein_identification.rstrip('\r\n')
        protein_identification = protein_identification.lower()

        return protein_identification

    def protein_description( self, header=None ):
        """
        Return the protein description from a Fasta header.

        Args:
            header(str): A Fasta header.

        Returns:
            (str): The protein description.
        """

        protein_description = header.split(' ')

        # Some headers has more then a single space as field separator.
        # So, we're changin all to a single space.
        #...
        # Pick all fields. That's a list.
        protein_description = protein_description[1:]

        # Join all the elements using white space as separator.
        protein_description = ' '.join( protein_description )

        # Change double white spaces by a single space.
        protein_description = re.sub(r"\ {1,}", " ", protein_description)

        # Remove white spaces at the beggining and at the end of the string.
        protein_description = re.sub(r"^\ ", "", protein_description)
        protein_description = re.sub(r"\ $", "", protein_description)

        # Remove this fucker that ruined hours of data importing.
        protein_description = protein_description.replace('\\','')
        
        # And who knows... quotes:
        protein_description = protein_description.replace('"','')

        return protein_description 

    def has_ec_from_square_brackets( self, header=None ):
        """
        Return True if the header has an EC annotation.

        It expect EC numbers surrounded by square brackets '[]'.

        That's a important observation because different versions of pep files relies on different marks to identify EC numbers.

        Args:
            header(str): A Fasta header.

        Returns:
            (boolean):
        """

        find_eC = re.compile('\[EC:')

        if find_eC.search( header ):
            return True
        else:
            return False


    def has_ec_from_brackets( self, header=None ):
        """
        Return True if the header has an EC annotation.

        It expect EC numbers surrounded by brackets '()'.

        That's a important observation because different versions of pep files relies on different marks to identify EC numbers.

        Args:
            header(str): A Fasta header.

        Returns:
            (boolean):
        """

        find_eC = re.compile('\(EC:')

        if find_eC.search( header ):
            return True
        else:
            return False


    def ec_from_square_brackets( self, header=None ):
        """
        Return the list of EC numbers from a Fasta header.

        This methods expect to find EC numbers surrounded by square brackets '[]'.

        That's a important observation since different versions of pep files relies on different marks to annotate EC numbers.

        Args:
            header(str): A Fasta header.

        Returns:
            (list): List of EC numbers identified in the Fasta header.
        """

        re_ec_number = re.compile('^>.*\[EC:(.*)\]')

        if self.has_ec_from_square_brackets( header ):
            ec_number_result = re_ec_number.search( header )
            
            ec_number = ec_number_result.group(1)
            ec_number = ec_number.split(' ')

            return ec_number

        else:

            return [] 

    def ec_from_brackets( self, header=None ):
        """
        Return the list of EC numbers from a Fasta header.

        This methods expect to find EC numbers surrounded by brackets '()'.

        That's a important observation since different versions of pep files relies on different marks to annotate EC numbers.

        Args:
            header(str): A Fasta header.

        Returns:
            (list): List of EC numbers identified in the Fasta header.
        """

        re_ec_number = re.compile('^>.*\(EC:(.*)\)')

        if self.has_ec_from_brackets( header ):
            ec_number_result = re_ec_number.search( header )
            
            ec_number = ec_number_result.group(1)
            ec_number = ec_number.split(' ')

            return ec_number

        else:

            return [] 


    def organism_code( self, header=None ):
        """
        Returns the 3 (or more) letters organism code from a Fasta header.

        Args:
            header(str): A Fasta header.

        Returns:
            (str): 3 (or more) letters organism code.
        """

        # Split by space
        organism_code = header.split(' ')
        
        # First field (like '>rno:2324')
        organism_code = organism_code[0]

        # Split by colon.
        organism_code = organism_code.split(':')

        # First field (like '>rno')
        organism_code = organism_code[0]

        # Remove the '>' char.
        # Considering the example in theese coments, final string should be 'rno'.
        organism_code = organism_code.replace('>','')

        return organism_code 


    def full_fasta_header( self, header=None ):
        """
        Simply return the full header.

        Args:
            header(str): A Fasta header.

        Returns:
            (str): The header itself. 
        """

        header = header.replace('\\','')
        header = header.replace('"','')

        return header
