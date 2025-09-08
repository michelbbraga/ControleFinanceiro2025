import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.investment import db
from src.routes.investment import investment_bp
from datetime import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

app.register_blueprint(investment_bp, url_prefix='/api')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_sample_data():
    """Inicializar dados de exemplo"""
    from src.models.investment import Acao, FII, TesouroDireto, RendaFixa
    
    # Verificar se já existem dados
    if Acao.query.first():
        return
    
    # Dados de exemplo
    acoes = [
        Acao(nome='VALE3', empresa='Vale S.A.', data_compra=datetime(2024, 1, 10).date(), 
             quantidade=50, preco_compra=65.00, preco_atual=70.00),
        Acao(nome='PETR4', empresa='Petrobras', data_compra=datetime(2024, 2, 15).date(), 
             quantidade=100, preco_compra=30.00, preco_atual=28.00)
    ]
    
    fiis = [
        FII(nome='MXRF11', empresa='Maxi Renda FII', data_compra=datetime(2023, 11, 20).date(), 
            quantidade=200, preco_compra=10.00, preco_atual=10.50),
        FII(nome='HGLG11', empresa='CSHG Logística', data_compra=datetime(2024, 3, 1).date(), 
            quantidade=50, preco_compra=160.00, preco_atual=158.00)
    ]
    
    tesouro = [
        TesouroDireto(nome='Tesouro Selic 2027', tipo='Pós-fixado', 
                     data_vencimento=datetime(2027, 3, 1).date(), tipo_pagamento='Juros Semestrais',
                     data_compra=datetime(2023, 5, 1).date(), quantidade=1, 
                     preco_compra=13000.00, preco_atual=13500.00, rentabilidade_prevista='Selic + 0.05%')
    ]
    
    renda_fixa = [
        RendaFixa(nome='CDB Banco X', instituicao='Banco X', 
                 data_vencimento=datetime(2025, 10, 20).date(), tipo_pagamento='Principal',
                 data_compra=datetime(2023, 8, 1).date(), quantidade=1, 
                 preco_compra=10000.00, preco_atual=10800.00, rentabilidade_prevista='110% CDI')
    ]
    
    for acao in acoes:
        db.session.add(acao)
    for fii in fiis:
        db.session.add(fii)
    for titulo in tesouro:
        db.session.add(titulo)
    for inv in renda_fixa:
        db.session.add(inv)
    
    db.session.commit()

with app.app_context():
    db.create_all()
    init_sample_data()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
