#!flask/bin/python

import flask
app = flask.Flask(__name__)

## data should usually come from a database...
genes = [
  {"gene_id": 1, "symbol": "ABC"},
  {"gene_id": 2, "symbol": "DEF"},
  {"gene_id": 3, "symbol": "GHI"}
]


# This method will get the info for a single gene by searching for it's gene_id.
# It returns the gene's json data, or 404 if not found.
@app.route('/v1/genes/<int:gene_id>', methods=['GET'])
def get_gene(gene_id):
    gene = [g for g in genes if g['gene_id'] == gene_id]
    if len(gene) == 0:
        flask.abort(404)
    return flask.jsonify({'gene': gene[0]})



# This method will add a new gene's data to the "database" above.
# If gene_id or symbol are not provided, returns HTTP Status 400 for bad request.
# It returns the gene's json data and HTTP Status 201 upon success.
@app.route('/v1/genes', methods=['POST'])
def create_gene():
    data = flask.request.json
    if not data or not 'symbol' in data or not 'gene_id' in data:
        flask.abort(400)
    g = {
        'gene_id': data['gene_id'],
        'symbol': data['symbol'],
        'description': data.get('description', "")
    }
    genes.append(g)
    return flask.jsonify({'gene': g}), 201



# This method will list the info for a all known genes.
# It returns the genes' json data in a list.
@app.route('/v1/genes', methods=['GET'])
def list_genes():
    return flask.jsonify({'genes': genes})



# Sets the default error handler to return a json error instead of text.
@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	app.run(debug=True)
