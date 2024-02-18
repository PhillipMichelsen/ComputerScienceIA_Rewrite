import logging
from io import BytesIO
from xml.etree import ElementTree

import requests


class GrobidClient:
    def __init__(self, grobid_url):
        self.grobid_url = grobid_url

    def process_file(self, object_key, file_bytes: BytesIO) -> str:
        files = {'input': (object_key, file_bytes)}
        data = {
            'consolidateHeader': '1',
            'consolidateCitations': '1',
        }
        logging.info(f"Sending file to Grobid for processing: {object_key}")
        response = requests.post(f"{self.grobid_url}/api/processFulltextDocument", files=files, data=data, timeout=500)
        if response.status_code == 200:
            logging.info(f"Grobid processing successful for file: {object_key}")
            return response.text
        else:
            raise Exception(f"Grobid processing failed with status code: {response.status_code}")

    @staticmethod
    def tei_to_divisions(tei_xml: str) -> list:
        root = ElementTree.fromstring(tei_xml)

        divisions = root.findall('.//tei:div', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        divisions = [' '.join(division.itertext()) for division in divisions]

        return divisions
