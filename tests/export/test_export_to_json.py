import json
import logging
import unittest
from pathlib import Path

from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(filename="../export/test-export-to-json.log", level=logging.DEBUG)


class TestExportToJSON(Test):
    """
    This test attempts to export each PDF in the corpus to JSON
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../export/test-export-to-json")

    def test_corpus(self):
        super(TestExportToJSON, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            doc = PDF.loads(pdf_file_handle)
            output_file = self.output_dir / (file.stem + ".json")

            # export to json
            with open(output_file, "w") as json_file_handle:
                json_file_handle.write(
                    json.dumps(doc.to_json_serializable(doc), indent=4)
                )

        return True


if __name__ == "__main__":
    unittest.main()
