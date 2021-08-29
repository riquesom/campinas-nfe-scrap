from bs4 import BeautifulSoup
from flask import request

import requests
from api.dictionary.nfe_data import nfe_dict, nfe_data


class NfeValidateModel:
    def __init__(self):

        cnpj = request.args.get("cnpj")
        numero_nota = request.args.get("numero_nota")
        codigo_verificacao = request.args.get("codigo_verificacao")
        inscricao_municipal = request.args.get("inscricao_municipal")
        self.result = self.get_validate(cnpj, numero_nota, codigo_verificacao, inscricao_municipal)
        self.error = False

    @staticmethod
    def get_validate(cnpj, numero_nota, codigo_verificacao, inscricao_municipal):

        if cnpj is None or numero_nota is None or codigo_verificacao is None or inscricao_municipal is None:
            raise Exception({'status_code': 406, 'result': 'Parâmetros inválidos.'})

        data = nfe_dict

        req = requests.Session()

        body = {'rPrest': str(cnpj),
                'rNumNota': str(numero_nota),
                'rInsMun': str(inscricao_municipal),
                'rCodigoVerificacao': str(codigo_verificacao),
                'cap_text': '',
                'rCodCid': '6291',
                'temPrestador': 'Tg==',
                'rCpfCnpj': '',
                'btnVerificar': 'Verificar'}
        ret = req.post(url='https://nfse.campinas.sp.gov.br/NotaFiscal/action/notaFiscal/verificarAutenticidade.php',
                       data=body)

        url_nfe = 'https://nfse.campinas.sp.gov.br/NotaFiscal/' + \
                  ret.text[ret.text.find('notaFiscal.php'):ret.text.find("','NFSE'")]

        nfe = req.get(url_nfe)

        soup = BeautifulSoup(nfe.text, 'html.parser')

        tables = soup.find_all('table', class_='impressaoTabela')

        for table in tables:
            if 'PRESTADOR DE SERVIÇOS' in table.text:
                tds = table.find_all('td', class_='impressaoLabel')
                for td in tds:
                    info = [x for x in nfe_data['prestador_servico'] if x['name'] in td.text]
                    if len(info) == 1:
                        data['prestador_servico'][info[0]['dict']] = td.span.text.strip()
            elif 'TOMADOR DE SERVIÇOS' in table.text:
                tds = table.find_all('td', class_='impressaoLabel')
                for td in tds:
                    info = [x for x in nfe_data['tomador_servico'] if x['name'] in td.text]
                    if len(info) == 1:
                        data['tomador_servico'][info[0]['dict']] = td.span.text.strip()

        return data
