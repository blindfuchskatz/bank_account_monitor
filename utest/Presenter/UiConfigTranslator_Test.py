import unittest
from src.Presenter.UiConfigTranslator import UiConfigTranslator


class AUiConfigTranslator(unittest.TestCase):

    def testAdd_csv_output_file(self):
        ui_conf_trans = UiConfigTranslator()
        p_config = ui_conf_trans.translate("/some/path", "")

        self.assertEqual(p_config.csv_output_file, "/some/path")

    def testTranslatePlotterData_title(self):
        ui_conf_trans = UiConfigTranslator()
        p_config = ui_conf_trans.translate("", "title")

        self.assertEqual(p_config.csv_output_file, "")
        self.assertEqual(p_config.title, "title")

    def testTranslatePlotterData_ignore_list(self):
        ui_conf_trans = UiConfigTranslator()

        c1 = ui_conf_trans.translate("", "title")
        c2 = ui_conf_trans.translate("", "title;")
        c3 = ui_conf_trans.translate("", "title;fund")
        c4 = ui_conf_trans.translate("", "title;fund;bank")

        self.assertEqual(c1.ignore_list, [])
        self.assertEqual(c2.ignore_list, [""])
        self.assertEqual(c3.ignore_list, ["fund"])
        self.assertEqual(c4.ignore_list, ["fund", "bank"])
