import logging

from pesquisa_nome_agendado.pdf_file_handler import get_text_page_number
from pesquisa_nome_agendado.scraper import download
from pesquisa_nome_agendado.file_handler import get_file_list_from_directory

logging.basicConfig(level=logging.INFO)

# file_name: str = 'Profissionais_da_saúde_D2__Agendados_-_dia_12-04-2021.pdf'


if __name__ == '__main__':
    download()
    for file_name in get_file_list_from_directory(directory='pdf'):
        page_in_which_text_was_found: int = get_text_page_number(
            search_text='JUNIOR CEZAR ALVES BATISTA',
            pdf_file_name=file_name)
        if page_in_which_text_was_found != -1:
            break
