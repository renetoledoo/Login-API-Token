# FastAPI Auth API

![Python](https://img.shields.io/badge/python-3.9-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.1-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

## Descrição

Esta é uma API simples desenvolvida com FastAPI para autenticação de usuários. Ela permite o cadastro e login de usuários, além de consultar a lista de usuários cadastrados.

## Endpoints

### Cadastro de Usuário
Cadastro de Usuário
POST /cadastro

- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
- 
- **Obter Usuários**: 
GET /usuarios

  ```json
  Utilizar String Param (token_param) :
  http://127.0.0.1:2020/usuarios?token_param=205d0f70631e4719dc278ae11b41d5


- **Execute a aplicação:**:  
  ```json
  uvicorn app.main:app --reload

- **Documentação API:**: 
![img.png](img.png)

![img_1.png](img_1.png)
