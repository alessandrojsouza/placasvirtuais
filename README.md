# Placas Virtuais - IFRN

> Projeto destinado a construção de um sistema web que gerência placas de formaturas virtuais.

Toda parte de documentação do projeto se encontra na pasta docs no diretório raiz do repositório.

## Funcionalidades

### Externamente

- [x] Visualização das últimas placas de formaturas;
- [x] Pesquisa pelas placas de formaturas;
- [x] Visualização detalhada das placas pesquisadas;
- [x] Visualização das placas por diretória do campus CNAT;
- [x] Login para usuários autenticados na plataforma.

### Internamente

- [x] Criação e ou importação via SUAP, listagem, edição e exclusão de Usuários;
- [x] Criação e ou importação via SUAP, listagem, edição e exclusão de Campus (opção para extender a plataforma para outros campus);
- [x] Criação e ou importação via SUAP, listagem, edição e exclusão de Cursos;
- [x] Criação e ou importação via SUAP, listagem, edição e exclusão de Egressos;
- [x] Criação, listagem, edição e exclusão das Placas de Formatura;
  - [x] Pode-se adicionar à placa Mencionados, Mensagem da turma, Imagem e mais detalhes da placa.

## Como desenvolver?

Desenvolvimento se dá através do host http://localhost:8000/.

```console
❯ git clone https://github.com/alessandrojsouza/placasvirtuais.git
❯ cd placasvirtuais/
❯ python3 -m venv .wnea
❯ source .wnea/bin/activate ou .wnea\Scripts\activate (windows)
❯ sudo apt-get install libpq-dev python3-dev python3-venv
❯ pip3 install -r requirements.txt
❯ cp .env-sample .env
❯ python3 manage.py makemigrations
❯ python3 manage.py migrate
❯ python3 manage.py runserver
```

### Configurações SUAP

As credentials do SUAP são provenientes da criação e configuração no site da https://suap.ifrn.edu.br/api/applications/ promovida via SUAP.
Onde após a criação da aplicação, são providas os dados:

- CLIENTE_ID
- CLIENT_SECRET
- TOKEN_SUAP_SECRET

\*Obs: lembrar de adicionar no campo `redirect_uris` a informação {host}/suap_login/.
Ex: http://localhost:8000/suap_login/.

## Como realizar build?

Essa aplicação utiliza dockerfile e docker-compose para produção.

```console
❯ // need create .env
❯ sudo docker-compose stop
❯ sudo docker-compose up -d --build
```
