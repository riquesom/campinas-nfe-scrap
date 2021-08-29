from flasgger import swag_from
from flask import Blueprint, jsonify, redirect, url_for

from api.model.nfe_validade import NfeValidateModel
from api.schema.nfe_validate import NfeValidateSchema

nfe_api = Blueprint('api', __name__)


@nfe_api.route('/nfe/validate')
@swag_from({
    'tags': ['NFE'],
    'parameters': [
        {'in': 'query',
         'name': 'cnpj',
         'type': 'string',
         'description': 'CNPJ do Prestador de Serviços',
         'required': True, },
        {'in': 'query',
         'name': 'numero_nota',
         'type': 'string',
         'description': 'Numero da NFSe',
         'required': True, },
        {'in': 'query',
         'name': 'codigo_verificacao',
         'type': 'string',
         'description': 'Código de Verificação da NFSe',
         'required': True, },
        {'in': 'query',
         'name': 'inscricao_municipal',
         'type': 'string',
         'description': 'Inscrição Municipal',
         'required': True, },
    ],
    'responses': {
        200: {
            'description': 'Retorna cabeçalho da NFE',
            'schema': NfeValidateSchema
        },
        406: {
            'description': 'Parâmetros para retorno faltando',
            'schema': NfeValidateSchema
        },
        500: {
            'description': 'Erro interno do servidor',
            'schema': NfeValidateSchema
        }
    }
})
def validate():
    try:
        result = NfeValidateModel()
        return NfeValidateSchema().dump(result), 200
    except Exception as e:
        return jsonify({'error': True,
                        'result': e.args[0]['result']}), e.args[0]['status_code']
