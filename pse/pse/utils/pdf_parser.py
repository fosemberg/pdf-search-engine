import base64
import json

import requests
from PyPDF2 import PdfFileWriter, PdfFileReader

from pse.pse.settings import IAM_TOKEN, FOLDER_ID


def split_file_to_pages(source_filename, open_file_func, write_output_func):
    """
    A function to split a PDF file into separate pages.
    :param source_filename: The name of the source multi-page file
    :param open_file_func: A function that takes a name of PDF file as an input and returns its contents
    :param write_output_func: A function that takes output file content and target filename and saves the content
    :return:
    Example:
    >>> split_file_to_pages('test', open_pdf, write_pdf)
    """
    infile = PdfFileReader(open_file_func(source_filename))
    for i in range(infile.getNumPages()):
        p = infile.getPage(i)
        write_output_func(p, filename=f'{source_filename}-{i}')


def open_pdf(filename):
    """
    A sample function to get the content of a PDF file.
    """
    return open(f'{filename}.pdf', 'rb')


def write_pdf(content, filename):
    """
    A sample function to write a single-paged PDF.
    """
    outfile = PdfFileWriter()
    outfile.addPage(content)
    with open(f'pages/{filename}.pdf', 'wb') as f:
        outfile.write(f)


API_URL = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {IAM_TOKEN}'
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


def parse_pdf(source_filename, open_file_func, write_output_func):
    """
    A function that uses Yandex.Vision to retrieve text from PDF.
    :param source_filename: The name of the source pdf file (<=8 pages)
    :param open_file_func: A function that takes a name of PDF file as an input and returns its contents
    :param write_output_func: A function that takes output text and saves it somewhere
    :return:
    Example:
    >>> parse_pdf('test', open_pdf, write_text)
    """
    file = open_file_func(source_filename)
    content = encode_file(file)
    payload["analyze_specs"][0]["content"] = content
    r = requests.post(
        API_URL,
        headers=HEADERS,
        data=json.dumps(payload),
    )
    parsed_text = parse_response(json.loads(r.text))
    write_output_func(parsed_text, source_filename)


def encode_file(file):
    """
    Prepare  the file content to be passed to Yandex.Cloud API.
    """
    file_content = file.read()
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


def write_text(content, filename):
    with open(f'{filename}.txt', "w") as file:
        file.write(content)
