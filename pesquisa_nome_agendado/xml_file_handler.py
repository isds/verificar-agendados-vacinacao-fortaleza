from xml.etree import ElementTree

from pesquisa_nome_agendado.settings import XML_FILE_NAME


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
