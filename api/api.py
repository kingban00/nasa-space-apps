from flask import Flask, jsonify, request
from iaTraining import fazer_previsao
from beautifulSoap import extract_elements_for_anchor
from joblib import load

app = Flask(__name__)

# Defina a rota da API
@app.route('/api/extract_data/<anchor>', methods=['GET'])
def get_data(anchor):
    base_url = "https://www.usgs.gov/science/science-explorer/climate"
    
    elements = extract_elements_for_anchor(base_url, anchor)
    
    if elements is not None:
        return jsonify(elements)
    else:
        return jsonify({'error': 'Failed to retrieve data for anchor'}), 500


@app.route('/api/consultar', methods=['POST'])
def consultar():
    modelo_categoria = load('modelo_categoria.joblib')
    modelo_agencia = load('modelo_agencia.joblib')
    modelo_topico = load('modelo_topico.joblib')
    vetorizador = load('vetorizador.joblib')

    consulta = request.json.get('consulta')

    if consulta is None:
        return jsonify({'error': 'Consulta ausente'}), 400

    categoria_predita, agencia_predita, topico_predito = fazer_previsao(consulta)

    resposta = {
        'categoria_predita': categoria_predita[0],
        'agencia_predita': agencia_predita[0],
        'topico_predito': topico_predito[0]
    }
    return jsonify(resposta)


if __name__ == '__main__':
    app.run(debug=True)