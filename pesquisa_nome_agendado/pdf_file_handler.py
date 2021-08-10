import logging
import os

import PyPDF2
from PyPDF2.pdf import PageObject

from pesquisa_nome_agendado.settings import PDF_DIRECTORY


def get_text_page_number(search_text: str, pdf_file_name: str) -> int:
    file_path: os = os.path.join(PDF_DIRECTORY, pdf_file_name)
    pdf_file_object = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

    number_of_pages: int = pdf_reader.getNumPages()
    for page_number in range(number_of_pages):
        logging.info(f"Procurando o termo '{search_text}' na página {page_number} do arquivo '{pdf_file_name}'")
        pdf_page: PageObject = pdf_reader.getPage(page_number)
        page_text: str = pdf_page.extractText()
        if search_text in page_text:
            logging.info(f'ENCONTROU NA PÁGINA nª {page_number} do arquivo {pdf_file_name}')
            return page_number
    return -1
