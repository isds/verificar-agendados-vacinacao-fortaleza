import logging
import os

from pesquisa_nome_agendado.download import download_file_content_from_url
from pesquisa_nome_agendado.settings import XML_DIRECTORY, XML_FILE_NAME, PDF_DIRECTORY, files_resource
from pesquisa_nome_agendado.xml_file_handler import get_lista_arquivos_from_xml


def download_reference_xml_file() -> None:
    download_file_content_from_url(
        file_name=XML_FILE_NAME,
        file_path=XML_DIRECTORY,
        url=files_resource
    )


def download_pdf_file(file_name: str, url: str) -> None:
    normalized_file_name = f'{file_name}.pdf'.replace(' ', '_').replace('/', '-')
    file_path = os.path.join(PDF_DIRECTORY, normalized_file_name)
    download_file_content_from_url(file_path=PDF_DIRECTORY, file_name=file_path, url=url)


def download_pdf_files_from_url_list() -> None:
    download_reference_xml_file()
    links: dict = get_lista_arquivos_from_xml()

    total: int = len(links.values())
    for index, (arquivo, link) in enumerate(links.items()):
        download_pdf_file(file_name=arquivo, url=link)
        logging.info(f'{index + 1} de um total de {total}')


def download():
    download_pdf_files_from_url_list()
