import os
import cv2
import numpy as np
from django.http import HttpResponse
from rest_framework import status
from wand.image import Image, Color
from PyPDF2 import PdfFileReader, PdfFileWriter
from utils import storage_upload


RESOLUTION = 150


def zero_runs(a):
    is_zero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    abs_diff = np.abs(np.diff(is_zero))
    ranges = np.where(abs_diff == 1)[0].reshape(-1, 2)
    return ranges


def extract_images(pdf_file):
    urls = dict()
    infile = PdfFileReader(pdf_file)
    for i in range(infile.getNumPages()):
        output_pdf = PdfFileWriter()
        output_pdf.addPage(infile.getPage(i))
        workpath = os.path.dirname(os.path.abspath(__file__))
        tem_pdf_path = os.path.join(workpath, 'temp_pdf.pdf')
        with open(tem_pdf_path, "wb") as out_file:
            output_pdf.write(out_file)
        with Image(filename=os.path.join(workpath, 'temp_pdf.pdf'), resolution=RESOLUTION) as img:
            with Image(width=img.width, height=img.height, background=Color("white")) as bg:
                bg.composite(img, 0, 0)
                bg.save(filename="tmp.png")

        img = cv2.imread('tmp.png', cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray_inverted = 255 - img_gray

        row_means = cv2.reduce(img_gray_inverted, 1, cv2.REDUCE_AVG, dtype=cv2.CV_32F).flatten()
        row_gaps = zero_runs(row_means)
        row_cutpoints = (row_gaps[:, 0] + row_gaps[:, 1] - 1) // 2

        urls[i] = []
        for n, (y1, y2) in enumerate(zip(row_cutpoints, row_cutpoints[1:])):
            y1 = int(y1)
            y2 = int(y2)

            line_gray_inverted = img_gray_inverted[y1:y2]

            column_means = cv2.reduce(line_gray_inverted, 0, cv2.REDUCE_AVG, dtype=cv2.CV_32F).flatten()
            column_gaps = zero_runs(column_means)
            column_gap_sizes = column_gaps[:, 1] - column_gaps[:, 0]
            column_cutpoints = (column_gaps[:, 0] + column_gaps[:, 1] - 1) // 2

            filtered_cutpoints = column_cutpoints[column_gap_sizes > 15]

            img_num = 0
            for x1, x2 in zip(filtered_cutpoints, filtered_cutpoints[1:]):

                # METRICS
                selected_column_means = column_means[x1:x2]
                non_0 = list(filter(None, selected_column_means))
                mean = np.sum(non_0) / len(non_0)
                max = np.max(non_0)

                if mean / max < 0.15 or mean > 120:
                    c = img.copy()
                    name = "img{}{}_at_page{}.png".format(img_num, n, i)
                    cv2.imwrite(name, c[y1:y2, x1:x2])
                    storage_response = storage_upload.file2url(name, name)
                    if storage_response['error'] is not None:
                        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    urls[i].append(storage_response['url'])
                    os.remove(name)
                    img_num += 1

        os.remove('tmp.png')
        os.remove(tem_pdf_path)
        return urls
