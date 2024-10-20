from fastapi import FastAPI
from model import engine, Pessoa, Tokens, PessoaModelo, LoginModelo
from secrets import token_hex
from sqlalchemy.orm import sessionmaker
import bcrypt
from datetime import datetime, timedelta

app = FastAPI(title='Login Authentication via Token with APi - Renê')

def conecta_banco():
    Session = sessionmaker(bind=engine)
    return Session()


@app.post('/cadastro')
def cadastro(modelo: PessoaModelo):
        session = conecta_banco()
        try:
            usuario_filtrado = session.query(Pessoa).filter_by(usuario=modelo.usuario).all()

            if len(usuario_filtrado) == 0:
                if len(modelo.senha) >= 6:
                    nova_senha = bcrypt.hashpw(modelo.senha.encode('UTF-8'), bcrypt.gensalt(10))
                    nova_pessoa = Pessoa(nome=modelo.nome, usuario=modelo.usuario, senha=nova_senha)
                    session.add(nova_pessoa)
                    session.commit()
                    return {'status': 'Usuário cadastrado com sucesso.'}
                else:
                    return {'status': 'A senha precisa ter mais de 6 caracteres.'}

            else:
                return {'status': 'Nome de usuário já existente.'}

        except Exception as e:
            session.rollback()
            print(f"Erro ao inserir usuário: {e}")
            return {'status': 'Não foi possível inserir o usuário'}


@app.post('/login')
def login(usuario: LoginModelo):
    session = conecta_banco()

    usuario_logado = session.query(Pessoa).filter_by(usuario=usuario.usuario).first()

    if usuario_logado and bcrypt.checkpw(usuario.senha.encode('UTF-8'), usuario_logado.senha.encode('UTF-8')):
        data_expiracao = datetime.now() + timedelta(days=1)

        while True:
            token = token_hex(15)
            token_existe = session.query(Tokens).filter_by(token=token).all()
            if len(token_existe) == 0:
                pessoa_existe = session.query(Tokens).filter_by(id_pessoa=usuario_logado.id).all()
                if len(pessoa_existe) == 0:
                    novo_token = Tokens(id_pessoa=usuario_logado.id, token=token, data_expiracao=data_expiracao)
                    session.add(novo_token)
                elif len(pessoa_existe) > 0:
                    pessoa_existe[0].tokens = token
                    pessoa_existe[0].data_expiracao = data_expiracao

            session.commit()
            break
        return token
    else:
        return {'status': 'Usuario ou senha incorreta.'}


@app.get('/usuarios')
def obter_usuarios(token_param: str):
    session = conecta_banco()
    try:
        token_banco = session.query(Tokens).filter_by(token=token_param).first()
        print(token_banco.data_expiracao)

        if (token_banco.data_expiracao > datetime.now()):
            usuarios = session.query(Pessoa).with_entities(Pessoa.nome, Pessoa.usuario).all()
            usuarios_retorno = [{'nome': nome, 'usuario': usuario} for nome, usuario in usuarios]
            return {'status': 'sucesso', 'dados': usuarios_retorno}
        else:
            return {'status': 'Token expirado.'}
    except Exception as e:
        print('Pilha de Depuração: ', e)
        return {'status': 'Não foi possivel obter usuários'}
    finally:
        session.close()