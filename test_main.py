from unittest import TestCase
import pandas as pd
import numpy as np
# noinspection PyUnresolvedReferences
import xlrd  # NB: needed for read_excel(), don't remove

import pathlib

from main import func_to_test

path_data_dir = pathlib.Path(__file__).parents[0]
path_unittests = path_data_dir / "Unit Tests v1.xlsx"


def load_unittests(path=path_unittests):
    """
    """
    df = pd.read_excel(str(path))
    df = df.reset_index().rename(columns={'index': 'EXCEL_ROW'})
    df['EXCEL_ROW'] = df['EXCEL_ROW'] + 2 # account for excel being 1-based, and the header row

    return df



class TestsFromFile(TestCase):
    """
    This is the bare class to which test cases will be added as they are read from the validations file.
    Process each analysis, one at a time.
    """

    def setUp(self):
        pass


def gen_test_case(record):
    def test(self):

        with self.subTest('check structure'):
            self.assertTrue('EXCEL_ROW' in record._fields)


        with self.subTest('check result'):
            result = func_to_test(record.a, record.b)
            self.assertEqual(record.result_expected, result)

    return test


unittests = load_unittests()


for record in unittests.itertuples(index=False, name='LoadedUnitTest'):
    recid = f"'{str(record.RECORD_ID)}'" if (('RECORD_ID' in record._fields) and (record.RECORD_ID == record.RECORD_ID)) else '<none>'
    recstr = f'EXCEL_ROW={str(record.EXCEL_ROW)} \t RECORD_ID={recid}'

    test_case_name = 'test_{}'.format(recstr)
    setattr(TestsFromFile,
            test_case_name,
            gen_test_case(record)
            )
