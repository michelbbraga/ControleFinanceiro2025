from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Acao(db.Model):
    __tablename__ = 'acoes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(10), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    data_compra = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_atual = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'empresa': self.empresa,
            'data_compra': self.data_compra.isoformat() if self.data_compra else None,
            'quantidade': self.quantidade,
            'preco_compra': self.preco_compra,
            'preco_atual': self.preco_atual,
            'rentabilidade_absoluta': (self.preco_atual - self.preco_compra) * self.quantidade if self.preco_atual else 0,
            'rentabilidade_percentual': ((self.preco_atual - self.preco_compra) / self.preco_compra) * 100 if self.preco_atual else 0
        }

class FII(db.Model):
    __tablename__ = 'fiis'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(10), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    data_compra = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_atual = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'empresa': self.empresa,
            'data_compra': self.data_compra.isoformat() if self.data_compra else None,
            'quantidade': self.quantidade,
            'preco_compra': self.preco_compra,
            'preco_atual': self.preco_atual,
            'rentabilidade_absoluta': (self.preco_atual - self.preco_compra) * self.quantidade if self.preco_atual else 0,
            'rentabilidade_percentual': ((self.preco_atual - self.preco_compra) / self.preco_compra) * 100 if self.preco_atual else 0
        }

class TesouroDireto(db.Model):
    __tablename__ = 'tesouro_direto'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    tipo_pagamento = db.Column(db.String(50), nullable=False)
    data_compra = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_atual = db.Column(db.Float, nullable=True)
    rentabilidade_prevista = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'tipo_pagamento': self.tipo_pagamento,
            'data_compra': self.data_compra.isoformat() if self.data_compra else None,
            'quantidade': self.quantidade,
            'preco_compra': self.preco_compra,
            'preco_atual': self.preco_atual,
            'rentabilidade_prevista': self.rentabilidade_prevista,
            'rentabilidade_absoluta': (self.preco_atual - self.preco_compra) * self.quantidade if self.preco_atual else 0,
            'rentabilidade_percentual': ((self.preco_atual - self.preco_compra) / self.preco_compra) * 100 if self.preco_atual else 0
        }

class RendaFixa(db.Model):
    __tablename__ = 'renda_fixa'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    instituicao = db.Column(db.String(100), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    tipo_pagamento = db.Column(db.String(50), nullable=False)
    data_compra = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_atual = db.Column(db.Float, nullable=True)
    rentabilidade_prevista = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'instituicao': self.instituicao,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'tipo_pagamento': self.tipo_pagamento,
            'data_compra': self.data_compra.isoformat() if self.data_compra else None,
            'quantidade': self.quantidade,
            'preco_compra': self.preco_compra,
            'preco_atual': self.preco_atual,
            'rentabilidade_prevista': self.rentabilidade_prevista,
            'rentabilidade_absoluta': (self.preco_atual - self.preco_compra) * self.quantidade if self.preco_atual else 0,
            'rentabilidade_percentual': ((self.preco_atual - self.preco_compra) / self.preco_compra) * 100 if self.preco_atual else 0
        }

