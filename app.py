from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def conectar_banco():
    conn = sqlite3.connect('sugestoes.db')
    return conn

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sugestoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_colaborador TEXT NOT NULL,
            setor TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT DEFAULT 'aberta',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def inicio():
    return jsonify({
        "mensagem": "API de Sugestões SOGE funcionando",
        "rotas": [
            "GET /sugestoes - listar sugestoes",
            "POST /sugestoes - criar sugestao",
            "PUT /sugestoes/<id>/status - atualizar status",
            "DELETE /sugestoes/<id> - deletar sugestao"
        ]
    })

@app.route('/sugestoes', methods=['GET'])
def listar_sugestoes():
    status_filtro = request.args.get('status')
    setor_filtro = request.args.get('setor')
    
    conn = conectar_banco()
    cursor = conn.cursor()
    
    query = "SELECT * FROM sugestoes"
    parametros = []
    
    if status_filtro or setor_filtro:
        query += " WHERE "
        condicoes = []
        
        if status_filtro:
            condicoes.append("status = ?")
            parametros.append(status_filtro)
        
        if setor_filtro:
            condicoes.append("setor = ?")
            parametros.append(setor_filtro)
        
        query += " AND ".join(condicoes)
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, parametros)
    sugestoes = cursor.fetchall()
    conn.close()
    
    lista_sugestoes = []
    for sugestao in sugestoes:
        lista_sugestoes.append({
            "id": sugestao[0],
            "nome_colaborador": sugestao[1],
            "setor": sugestao[2],
            "descricao": sugestao[3],
            "status": sugestao[4],
            "data_criacao": sugestao[5]
        })
    
    return jsonify(lista_sugestoes)

@app.route('/sugestoes', methods=['POST'])
def criar_sugestao():
    dados = request.get_json()
    
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400
    
    if not dados.get('nome_colaborador'):
        return jsonify({"erro": "Nome do colaborador é obrigatório"}), 400
    
    if not dados.get('setor'):
        return jsonify({"erro": "Setor é obrigatório"}), 400
    
    if not dados.get('descricao'):
        return jsonify({"erro": "Descrição é obrigatória"}), 400
    
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sugestoes (nome_colaborador, setor, descricao)
        VALUES (?, ?, ?)
    ''', (dados['nome_colaborador'], dados['setor'], dados['descricao']))
    
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        "mensagem": "Sugestão criada com sucesso",
        "id": novo_id
    }), 201

@app.route('/sugestoes/<int:id>/status', methods=['PUT'])
def atualizar_status(id):
    dados = request.get_json()
    
    if not dados or not dados.get('status'):
        return jsonify({"erro": "Status é obrigatório"}), 400
    
    novo_status = dados['status']
    
    status_validos = ['aberta', 'em análise', 'implementada']
    if novo_status not in status_validos:
        return jsonify({"erro": "Status inválido"}), 400
    
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM sugestoes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Sugestão não encontrada"}), 404
    
    cursor.execute("UPDATE sugestoes SET status = ? WHERE id = ?", (novo_status, id))
    conn.commit()
    conn.close()
    
    return jsonify({"mensagem": "Status atualizado com sucesso"})

@app.route('/sugestoes/<int:id>', methods=['DELETE'])
def deletar_sugestao(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Verificar se a sugestão existe
    cursor.execute("SELECT id FROM sugestoes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"erro": "Sugestão não encontrada"}), 404
    
    # Deletar a sugestão
    cursor.execute("DELETE FROM sugestoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"mensagem": "Sugestão deletada com sucesso"})

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)