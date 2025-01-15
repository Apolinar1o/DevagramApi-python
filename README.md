# Instagram Clone Simplificado

Este projeto foi desenvolvido durante o treinamento da Devaria em 2023,
com base na funcionalidade principal do Instagram. 
O objetivo do projeto foi criar um clone simplificado do Instagram, 
implementando recursos fundamentais do aplicativo.

## Funcionalidades Implementadas

- Cadastro de usuários
- Login de usuários
- Publicação de fotos 
- Comentários em publicações
- Curtidas em publicações
- Pesquisa de usuários
- Perfis de usuários

## Tecnologias Utilizadas

- Python (linguagem de programação)
- FastApi (framework)
- Pydantic (para validação de dados)
- AWS S3 (para armazenamento de imagens)
- JWT (JSON Web Tokens) para criptografia e autenticação de usuários


## Pré-requisitos

- Visual Studio 2022 (ou versão mais recente)
-Python 3.8 ou superior
- Dependências do projeto (instaladas via pip install -r requirements.txt)
- Conta na AWS e configuração do S3 para o armazenamento das imagens

## Como Executar o Projeto

1. Faça o clone deste repositório para sua máquina local:`git clone <git@github.com:Apolinar1o/DevagramApi-python.git>`
2. Abra o Visual Studio e carregue a solução do projeto.
3. Instale as dependências do projeto com o comando:`pip install -r requirements.txt`
4. Configure suas credenciais do AWS S3 e outras variáveis no arquivo .env (por exemplo, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, e BUCKET_NAME).
5. uvicorn main:app --reload
6. Abra um navegador da web e acesse a URL `http://localhost:porta`, substituindo "porta" pela porta em que o projeto está sendo executado.

#
## Agradecimentos

Agradeço à equipe da Devaria pelo treinamento e suporte durante o desenvolvimento deste projeto. 

#
### Autor
* **Antônio Apolinário**
