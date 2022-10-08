from Darstellung.Darstellung import Darstellung
import unittest

class TestDarstellung (unittest.TestCase):

    def table_import(self):
        d = Darstellung()
        #self.assertEqual(d.table,Datenhaltung.get_table(), "Should be the same")

    def dimension_import(self):
        d = Darstellung()
        #self.assertEqual(d.room_dimension,Datenhaltung.get_room_data(), "Should be the same");

    def person_import(self):
        d = Darstellung
        #self.assertEqual(?, ?, "Should be the same")


if __name__ == '__main__':
    unittest.main()