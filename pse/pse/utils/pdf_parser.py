from PyPDF2 import PdfFileWriter, PdfFileReader


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

