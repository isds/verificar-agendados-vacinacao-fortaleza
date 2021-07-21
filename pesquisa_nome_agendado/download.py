import requests

from pesquisa_nome_agendado.exception import log_error
from pesquisa_nome_agendado.file_saver import save_file


def get_response_content(url: str) -> bytes:
    try:
        response = requests.get(url)
        return response.content
    except requests.ConnectionError as exception:
        log_error(
            exception,
            message='Erro ao acessar lista no google spreadsheets. Erro de conexão, a rede pode estar instável.')
    except requests.HTTPError as exception:
        log_error(
            exception,
            message='Erro ao acessar lista no google spreadsheets. Resposta HTTP inválida ou não reconhecida.')
    except requests.Timeout as exception:
        log_error(
            exception,
            message='Erro ao acessar lista no google spreadsheets. O tempo máximo de espera foi excedido.')
    except requests.TooManyRedirects as exception:
        log_error(
            exception,
            message='Erro ao acessar lista no google spreadsheets. O número máximo de redirecionamentos foi excedido')
    except requests.RequestException as exception:
        log_error(
            exception,
            message='Erro ao acessar lista no google spreadsheets. O erro e conexão não mapeado')


def download_file_content_from_url(file_path: str, file_name: str, url: str) -> None:
    content: bytes = get_response_content(url=url)
    save_file(file_content=content, path=file_path, file_name=file_name)
