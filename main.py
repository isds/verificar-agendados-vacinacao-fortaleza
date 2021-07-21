import logging

from pesquisa_nome_agendado.scraper import download


logging.basicConfig(level=logging.INFO)

file_name: str = 'Profissionais_da_saúde_D2__Agendados_-_dia_12-04-2021.pdf'


if __name__ == '__main__':
    download()
    # search_text_in_pdf_file(
    #     search_text='JUNIOR CEZAR ALVES BATISTA',
    #     pdf_file_name=file_name)
