import base64
import json

import requests
from PyPDF2 import PdfFileWriter, PdfFileReader
import io

from pse.settings import API_KEY, FOLDER_ID


def split_file_to_pages(file):
    """
    A function to split a PDF file into separate pages.
    :param file: A PDF file object
    :return:
    """
    infile = PdfFileReader(file)
    pages = []
    for i in range(infile.getNumPages()):
        tmp = io.BytesIO()
        p = infile.getPage(i)
        outfile = PdfFileWriter()
        outfile.addPage(p)
        outfile.write(tmp)
        pages.append(tmp)
    return pages


API_URL = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {API_KEY}'
}
payload = {
    "folderId": FOLDER_ID,
    "analyze_specs": [{
        "features": [{
            "type": "TEXT_DETECTION",
            "text_detection_config": {
                "language_codes": ["*"]
            }
        }],
        "mime_type": "application/pdf",
    }]
}


def parse_pdf(file):
    """
    A function that uses Yandex.Vision to retrieve text from PDF.
    :param file:The source pdf file (<=8 pages)
    :return: (response_text, parsed_text)
    """
    content = encode_file(file)
    payload["analyze_specs"][0]["content"] = content
    r = requests.post(
        API_URL,
        headers=HEADERS,
        data=json.dumps(payload),
    )
    response_text = json.loads(r.text)
    parsed_text = parse_response(response_text)
    return response_text, parsed_text


def encode_file(file):
    """
    Prepare  the file content to be passed to Yandex.Cloud API.
    """
    file_content = file.getvalue()
    return base64.b64encode(file_content).decode("utf-8")


def parse_response(response):
    """
    Parse the Yandex.Cloud API response to extract all text.
    """
    output_string = ''
    for result in response['results']:
        for res in result['results']:
            for page in res['textDetection']['pages']:
                for block in page['blocks']:
                    for line in block['lines']:
                        for word in line['words']:
                            output_string += ' '
                            output_string += word['text']
    return output_string
