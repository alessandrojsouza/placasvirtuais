# Placas Virtuais - IFRN

> Projeto destinado a construção de um sistema web que gerência placas de formaturas virtuais.

Toda parte de documentação do projeto se encontra na pasta docs no diretório raiz do repositório.

## Protótipo

[Figma](#)

## Como desenvolver?

Desenvolvimento se dá através do host http://localhost:8000/

```console
❯ git clone https://github.com/alessandrojsouza/placasvirtuais.git
❯ cd placasvirtuais/
❯ python3 -m venv .wnea
❯ source .wnea/bin/activate ou .wnea\Scripts\activate (windows)
❯ pip3 install -r requirements.txt
❯ cp contrib/env-sample .env
❯ python3 manage.py makemigrations
❯ python3 manage.py migrate
❯ python3 manage.py runserver
```
