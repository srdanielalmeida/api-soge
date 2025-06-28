API de Sugestões SOGE

Sistema para gerenciar sugestões de melhorias internas da empresa.

Como usar

Instalação

1. Instalar dependências:

pip install -r requirements.txt

2. Executar a API:

python app.py

3. A API estará disponível em: http://127.0.0.1:5000

Funcionalidades

- Cadastrar novas sugestões
- Listar todas as sugestões  
- Filtrar sugestões por status ou setor
- Atualizar status das sugestões

Como testar

Listar sugestões

GET http://127.0.0.1:5000/sugestoes

Filtrar por status

GET http://127.0.0.1:5000/sugestoes?status=aberta

Filtrar por setor

GET http://127.0.0.1:5000/sugestoes?setor=TI

Criar nova sugestão

POST http://127.0.0.1:5000/sugestoes
Content-Type: application/json

{
  "nome_colaborador": "João Silva",
  "setor": "TI",
  "descricao": "Melhorar sistema de backup"
}

Atualizar status

PUT http://127.0.0.1:5000/sugestoes/1/status
Content-Type: application/json

{
  "status": "em análise"
}


Campos da sugestão

- id: gerado automaticamente
- nome_colaborador: nome de quem fez a sugestão
- setor: setor da empresa
- descricao: descrição da sugestão
- status: aberta, em análise ou implementada
- data_criacao: criada automaticamente

Status válidos

- aberta
- em análise  
- implementada

Estrutura do banco

O sistema usa SQLite e cria automaticamente uma tabela chamada 'sugestoes' com os campos necessários.

Tecnologias usadas

- Python
- Flask
- SQLite