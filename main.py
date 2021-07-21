from pesquisa_nome_agendado.scraper import download_arquivos_pdf, search_text_in_pdf_file


if __name__ == '__main__':
    # download_arquivos_pdf()
    search_text_in_pdf_file(
        search_text='JUNIOR CEZAR ALVES BATISTA',
        pdf_file_name='Profissionais_da_saúde_D2__Agendados_-_dia_12-04-2021.pdf')
