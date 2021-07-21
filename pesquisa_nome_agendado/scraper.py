import os

from enum import Enum

import PyPDF2
import requests
import traceback
from xml.etree import ElementTree
import logging

from PyPDF2.pdf import PageObject

XML_DIRECTORY: str = 'xml'
XML_FILE_NAME: str = os.path.join(XML_DIRECTORY, 'lista_agendados.xml')
PDF_DIRECTORY: str = 'pdf'


class TipoExtensao(Enum):
    PDF = 'pdf'
    XML = 'xml'


def get_response_content(url: str) -> bytes:
    try:
        response = requests.get(url)
        return response.content
    except requests.ConnectionError as exception:
        log_error(exception, message='Erro ao acessar lista no google spreadsheets. Erro de conexão, a rede pode estar instável.')
    except requests.HTTPError as exception:
        log_error(exception, message='Erro ao acessar lista no google spreadsheets. Resposta HTTP inválida ou não reconhecida.')
    except requests.Timeout as exception:
        log_error(exception, message='Erro ao acessar lista no google spreadsheets. O tempo máximo de espera foi excedido.')
    except requests.TooManyRedirects as exception:
        log_error(exception, message='Erro ao acessar lista no google spreadsheets. O número máximo de redirecionamentos foi excedido')
    except requests.RequestException as exception:
        log_error(exception, message='Erro ao acessar lista no google spreadsheets. O erro e conexão não mapeado')


def log_error(exception, message: str):
    logging.error(message)
    logging.error(exception)
    traceback.print_exc()


def download_file_content(file_path: str, file_name: str, url: str) -> None:
    content: bytes = get_response_content(url=url)
    save_file(file_content=content, path=file_path, file_name=file_name)


def download_xml_file() -> None:
    download_file_content(
        file_name=XML_FILE_NAME,
        file_path=XML_DIRECTORY,
        url='https://spreadsheets.google.com/feeds/list/1IJBDu8dRGLkBgX72sRWKY6R9GfefsaDCXBd3Dz9PZNs/14/public/values'
    )


def save_file(file_content: bytes, path: str, file_name: str):
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(file_name, 'wb') as _file:
        _file.write(file_content)


def get_lista_arquivos_from_xml() -> dict:
    root = ElementTree.parse(XML_FILE_NAME).getroot()
    entries = root.findall('{http://www.w3.org/2005/Atom}entry')
    titulo = '{http://schemas.google.com/spreadsheets/2006/extended}titulo'
    pdf = '{http://schemas.google.com/spreadsheets/2006/extended}pdf'
    links: dict = {}
    for entry in entries:
        arquivo: str = entry.find(titulo).text
        link: str = entry.find(pdf).text
        if link.startswith('./pdfs/listas/'):
            link = f"https://coronavirus.fortaleza.ce.gov.br/{link.replace('./pdfs/listas/', 'pdfs/listas/')}"
        links[arquivo] = link
    return links


def download_pdf_file(file_name: str, url: str) -> None:
    normalized_file_name = f'{file_name}.pdf'.replace(' ', '_').replace('/', '-')
    file_path = os.path.join(PDF_DIRECTORY, normalized_file_name)
    download_file_content(file_path=PDF_DIRECTORY, file_name=file_path, url=url)


def download_arquivos_pdf() -> None:
    download_xml_file()
    links: dict = get_lista_arquivos_from_xml()

    total: int = len(links.values())
    for index, (arquivo, link) in enumerate(links.items()):
        download_pdf_file(file_name=arquivo, url=link)
        logging.info(f'{index + 1} de um total de {total}')


def search_text_in_pdf_file(search_text: str, pdf_file_name: str):
    file_path: os = os.path.join(PDF_DIRECTORY, pdf_file_name)
    pdf_file_object = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

    number_of_pages: int = pdf_reader.getNumPages()
    for page_number in range(number_of_pages):
        pdf_page: PageObject = pdf_reader.getPage(page_number)
        page_text: str = pdf_page.extractText()
        if search_text in page_text:
            print(f'ENCONTROU NA PÁGINA {page_number} do arquivo {pdf_file_name}')
