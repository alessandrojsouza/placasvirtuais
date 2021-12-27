# Placas Virtuais - IFRN

> Projeto destinado a construção de um sistema web que gerência placas de formaturas virtuais.

Toda parte de documentação do projeto se encontra na pasta docs no diretório raiz do repositório.

## Funcionalidades

### Externamente

- [ ] Visualização das últimas placas de formaturas;
- [ ] Pesquisa pelas placas de formaturas;
- [ ] Visualização detalhada das placas pesquisadas;
- [ ] Visualização das placas por diretória do campus CNAT;
- [ ] Login para usuários autenticados na plataforma.

### Internamente

- [ ] Criação e ou importação via SUAP, listagem, edição e exclusão de Usuários;
- [ ] Criação e ou importação via SUAP, listagem, edição e exclusão de Campus (opção para extender a plataforma para outros campus);
- [ ] Criação e ou importação via SUAP, listagem, edição e exclusão de Cursos;
- [ ] Criação e ou importação via SUAP, listagem, edição e exclusão de Egressos;
- [ ] Criação, listagem, edição e exclusão das Placas de Formatura;
  - [ ] Pode-se adicionar à placa Mencionados, Mensagem da turma, Imagem e mais detalhes da placa.

## Como desenvolver?

Desenvolvimento se dá através do host http://localhost:8000/.

As credentials do SUAP são provenientes da criação e configuração no site da https://suap.ifrn.edu.br/api/applications/ promovida pelo SUAP.

```console
❯ git clone https://github.com/alessandrojsouza/placasvirtuais.git
❯ cd placasvirtuais/
❯ python3 -m venv .wnea
❯ source .wnea/bin/activate ou .wnea\Scripts\activate (windows)
❯ sudo apt-get install libpq-dev python3-dev python3-venv
❯ pip3 install -r requirements.txt
❯ cp contrib/env-sample .env
❯ python3 manage.py makemigrations
❯ python3 manage.py migrate
❯ python3 manage.py runserver
```

## Como realizar build?

Essa aplicação utiliza dockerfile e docker-compose para produção.

```console
❯ // need create .env
❯ sudo docker-compose stop
❯ sudo docker-compose up -d --build
```
