import unittest

from pybtex.database.input import bibtex

from unused_bibtex_cleanup import get_citations_in_folder, write_new_bibtex_file


class BibtexDeletionTest(unittest.TestCase):

    def test_finding_citations(self):
        found_citations = get_citations_in_folder('test/resources/tex_folder')
        print(f'Found citations: {found_citations}')

        citations_to_find = ['StandardCitation', 'DoubleCitation1', 'DoubleCitation2', 'TripleCitation1',
                             'TripleCitation2', 'TripleCitation3', 'NatbibP', 'NatbibT', 'NatbibPStar', 'NatbibTStar',
                             'NatbibAuthor', 'NatbibYear', 'CommentCitation3', 'NatbibArg1', 'NatbibArg2']

        self.assertEqual(len(citations_to_find), len(found_citations))

        for cit in citations_to_find:
            self.assertIn(cit, found_citations)

    def test_deleting_citations(self):
        test_set = {'smit54', 'colu92', 'phil99'}
        bib_file_input_path = 'test/resources/testbib.bib'
        bib_file_output_path = 'test/resources/testbib_output.bib'

        write_new_bibtex_file(test_set, bib_file_input_path, False, False,
                              export_file_path=bib_file_output_path)

        # read exported file and check
        bib_file = bibtex.Parser().parse_file(bib_file_output_path)

        self.assertSetEqual(test_set, set(bib_file.entries.keys()))
        self.assertEqual(len(test_set), len(bib_file.entries))
