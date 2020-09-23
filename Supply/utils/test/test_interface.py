import unittest
import os
import shutil
from utils.interface import load_yaml, empty_folder, save_to_file


class TestIO(unittest.TestCase):
    def setUp(self):
        os.mkdir('temp')
        os.mkdir('do_not_empty')

    def tearDown(self):
        shutil.rmtree('temp')
        shutil.rmtree('do_not_empty')

    def test_load_yaml(self):
        parameters = load_yaml('parameters.yaml')
        self.assertIsNotNone(parameters)

    def test_empty_folder(self):
        open('temp/yes.txt', 'w')
        open('temp/no.txt', 'w')
        os.mkdir('temp/nest')
        open('temp/nest/wow.txt', 'w')
        empty_folder('temp')
        files = os.listdir('temp')
        self.assertEqual(len(files), 0)

        self.assertNotEqual(empty_folder('do_not_empty'), 0)

    def test_save_to_file(self):
        item = 'hello there'
        save_to_file(item, 'temp', 'hello.txt', output_status=False)
        self.assertEquals(item, open(
            'temp/hello.txt', 'r').read())
