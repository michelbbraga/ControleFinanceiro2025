from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case, text
from datetime import date
from sqlalchemy.dialects import sqlite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-key'
db = SQLAlchemy(app)

# ---------------- Models ----------------

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    categoria = db.Column(db.String(50), nullable=True)  # opcional (ex: alimentação, salário)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False, default=date)
    cd_payment_type = db.Column(db.Integer, nullable=True)

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    valor_meta = db.Column(db.Float, nullable=False)
    valor_acumulado = db.Column(db.Float, nullable=False, default=0.0)
    cd_goal_importance = db.Column(db.Integer, nullable=True)
    prazo = db.Column(db.Date, nullable=True)

class Investment(db.Model):
    __tablename__ = 'investments'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)  # 'acoes', 'renda_fixa', 'tesouro_direto', 'fiis'
    corretora = db.Column(db.String(100), nullable=True)
    nome_investimento = db.Column(db.String(200), nullable=False)
    nome_empresa = db.Column(db.String(200), nullable=True)
    data_compra = db.Column(db.Date, nullable=True)
    data_vencimento = db.Column(db.Date, nullable=True)
    valor_investido = db.Column(db.Float, nullable=False, default=0.0)
    taxa_retorno = db.Column(db.Float, nullable=True)  # em % ao ano, quando aplicável
    cd_indexer = db.Column(db.String(40), nullable=True)

class payment_type(db.Model):
    __tablename__ = 'payment_type'
    id = db.Column(db.Integer, primary_key=True)
    name_payment_type = db.Column(db.String(60), nullable=True)

class Indexer(db.Model):
    _tablename_= 'indexer'
    id = db.Column(db.Integer, primary_key=True)
    name_indexer = db.Column(db.String(40), nullable=False)

class goals_importance(db.Model):
    _tablename_= 'goals_importance'
    id = db.Column(db.Integer, primary_key=True)
    dc_goal_importance = db.Column(db.String(50), nullable=True)

# ---------------- Helpers ----------------

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def money(n):
    return f"R$ {n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

app.jinja_env.filters['money'] = money

# ---------------- Routes ----------------

@app.route('/init-db')
def init_db():
    db.create_all()
    flash("Banco de dados inicializado.", "success")
    return redirect(url_for('dashboard'))

@app.route('/')
def dashboard():
    # KPIs
    receitas = db.session.query(func.coalesce(func.sum(case((Transaction.tipo=='receita', Transaction.valor), else_=0)), 0)).scalar() or 0
    despesas = db.session.query(func.coalesce(func.sum(case((Transaction.tipo=='despesa', Transaction.valor), else_=0)), 0)).scalar() or 0
    saldo = receitas - despesas

    # Investimentos por categoria
    soma_por_categoria = db.session.query(Investment.categoria, func.coalesce(func.sum(Investment.valor_investido), 0))\
                                   .group_by(Investment.categoria).all()
    inv_por_categoria = {cat: total for cat, total in soma_por_categoria}

    # Progresso das metas
    metas = Goal.query.all()

    # Últimas transações
    ultimas_transacoes = Transaction.query.order_by(Transaction.data.desc(), Transaction.id.desc()).limit(8).all()

    return render_template('dashboard.html',
                           receitas=receitas, despesas=despesas, saldo=saldo,
                           inv_por_categoria=inv_por_categoria, metas=metas,
                           ultimas_transacoes=ultimas_transacoes)

# --------- Transações (Receitas/Despesas) ---------

@app.route('/transacoes', methods=['GET', 'POST'])
def transacoes():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        categoria = request.form.get('categoria') or None
        descricao = request.form.get('descricao')
        valor = float(request.form.get('valor') or 0)
        dc_tipo_pagamento = request.form.get('tipo_pagamento')
        data = parse_date(request.form.get('data')) or datetime.utcnow().date()

        cd_tipo_pagameto = db.session.query(payment_type).filter_by(name_payment_type=dc_tipo_pagamento).first()
        cd_pay_type = cd_tipo_pagameto.id
        

        if tipo not in ('receita', 'despesa'):
            flash('Tipo inválido.', 'danger')
        elif not descricao or valor <= 0:
            flash('Preencha descrição e valor (> 0).', 'danger')
        else:
            db.session.add(Transaction(tipo=tipo, categoria=categoria, descricao=descricao, valor=valor, data=data, cd_payment_type=cd_pay_type,))
            db.session.commit()
            flash('Lançamento salvo!', 'success')
        return redirect(url_for('transacoes'))

    # GET
    dt_ini = (date.today().year, date.today().month, 1)
    dt_fim= date.today()
    dt_ini2 = date(*dt_ini)
    #python_date_object_ini = datetime.strptime(dt_ini, "%Y-%m-%d").date()
    #python_date_object_fim = datetime.strptime(dt_fim, "%Y-%m-%d").date()
    print("teste ", type(dt_ini2), type(dt_fim))
    print("teste ", dt_ini2, dt_fim)
    trans = Transaction.query.order_by(Transaction.data.desc(), Transaction.id.desc()).all()
    trans_total = Transaction.query.filter(Transaction.data >= dt_ini2,
                                           Transaction.data <= dt_fim).all()
    print("teste ", trans_total)
    total_receitas = sum(t.valor for t in trans_total if t.tipo == 'receita')
    total_despesas = sum(t.valor for t in trans_total if t.tipo == 'despesa')
    payment_tp = payment_type.query.all()
    return render_template('transacoes.html', transacoes=trans, total_receitas=total_receitas, total_despesas=total_despesas, payment_type=payment_tp,)

# ---------------- Metas & Projetos ----------------

@app.route('/metas', methods=['GET', 'POST'])
def metas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        valor_meta = float(request.form.get('valor_meta') or 0)
        valor_acumulado = float(request.form.get('valor_acumulado') or 0)
        nivel_importancia = request.form.get('nivel_importancia')
        prazo = parse_date(request.form.get('prazo'))

        nv_importancia = db.session.query(goals_importance).filter_by(dc_goal_importance=nivel_importancia).first()
        id_nv_importancia = nv_importancia.id

        if not nome or valor_meta <= 0:
            flash('Preencha o nome e um valor de meta > 0.', 'danger')
        else:
            db.session.add(Goal(nome=nome, valor_meta=valor_meta, valor_acumulado=valor_acumulado, prazo=prazo, cd_goal_importance=id_nv_importancia))
            db.session.commit()
            flash('Meta salva!', 'success')
        return redirect(url_for('metas'))

    metas = Goal.query.order_by(Goal.prazo.asc().nullsLast()).all() if hasattr(db.text(''), 'nullsLast') else Goal.query.all()
    goal_importance = goals_importance.query.all()
    return render_template('metas.html', metas=metas, goal_importance=goal_importance,)

# ---------------- Investimentos ----------------

CATEGORIAS_VALIDAS = ['acoes', 'renda_fixa', 'tesouro_direto', 'fiis']

@app.route('/investimentos/<categoria>', methods=['GET', 'POST'])
def investimentos(categoria):
    if categoria not in CATEGORIAS_VALIDAS:
        flash('Categoria inválida.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        corretora = request.form.get('corretora')
        nome_investimento = request.form.get('nome_investimento')
        nome_empresa = request.form.get('nome_empresa') or None
        data_compra = parse_date(request.form.get('data_compra'))
        data_vencimento = parse_date(request.form.get('data_vencimento'))
        valor_investido = float(request.form.get('valor_investido') or 0)
        indexador = request.form.get('indexador') or None
        taxa_retorno = float(request.form.get('taxa_retorno') or 0) if request.form.get('taxa_retorno') else None

        name_indexer = db.session.query(Indexer).filter_by(name_indexer=indexador).first()

        if not nome_investimento or valor_investido <= 0:
            flash('Informe ao menos o nome do investimento e um valor > 0.', 'danger')
        else:
            inv = Investment(categoria=categoria, corretora=corretora, nome_investimento=nome_investimento,
                             nome_empresa=nome_empresa, data_compra=data_compra, data_vencimento=data_vencimento,
                             valor_investido=valor_investido, taxa_retorno=taxa_retorno)
            db.session.add(inv)
            db.session.commit()
            flash('Investimento cadastrado!', 'success')
        return redirect(url_for('investimentos', categoria=categoria))

    investimentos = Investment.query.filter_by(categoria=categoria).order_by(Investment.data_compra.desc().nullsLast()).all() if hasattr(db.text(''), 'nullsLast') else Investment.query.filter_by(categoria=categoria).all()
    total_categoria = sum(i.valor_investido for i in investimentos)
    index_invest = Indexer.query.all()
    return render_template('investimentos.html', investimentos=investimentos, categoria=categoria, total_categoria=total_categoria, index_invest=index_invest,)


# --------- Edições  ---------

@app.route('/meta_editar/<int:gide>', methods=['GET', 'POST'])
def meta_editar(gide):
    #meta_editar = Transaction.query.get_or_404(gide)
    print("teste-1", gide)
    if request.method== 'POST':
        nivel_importancia = request.form.get('nivel_importancia')
        with app.app_context():
            meta_editar = Goal.query.filter_by(id=gide).first()
            meta_editar.nome = request.form.get('nome')
            meta_editar.valor_meta = float(request.form.get('valor_meta') or 0)
            meta_editar.valor_acumulado = float(request.form.get('valor_acumulado') or 0)
            meta_editar.prazo = parse_date(request.form.get('prazo'))

            nv_importancia = db.session.query(goals_importance).filter_by(dc_goal_importance=nivel_importancia).first()
            id_nv_importancia = nv_importancia.id
            meta_editar.cd_goal_importance = id_nv_importancia

            db.session.commit()
            flash('Transação Atualizada.', 'info')
    
        return redirect(url_for('metas'))

    metas = Goal.query.order_by(Goal.prazo.asc().nullsLast()).all() if hasattr(db.text(''), 'nullsLast') else Goal.query.all()
    meta_editar = db.session.query(Goal).filter_by(id=gide).first()
    goal_importance = goals_importance.query.all()
    #print("teste-3", meta_editar.nome)
    #print("teste-4", metas)
    return render_template('meta_editar.html', metas=metas, meta_editar=meta_editar, goal_importance=goal_importance,)

# --------- Remoções simples ---------

@app.post('/transacoes/<int:tid>/excluir')
def excluir_transacao(tid):
    t = Transaction.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    flash('Transação excluída.', 'info')
    return redirect(url_for('transacoes'))

@app.post('/metas/<int:gid>/excluir')
def excluir_meta(gid):
    g = Goal.query.get_or_404(gid)
    db.session.delete(g)
    db.session.commit()
    flash('Meta excluída.', 'info')
    return redirect(url_for('metas'))

@app.post('/investimentos/<int:iid>/excluir')
def excluir_investimento(iid):
    i = Investment.query.get_or_404(iid)
    categoria = i.categoria
    db.session.delete(i)
    db.session.commit()
    flash('Investimento excluído.', 'info')
    return redirect(url_for('investimentos', categoria=categoria))

# ---------------- Run ----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
