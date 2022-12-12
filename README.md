# Smart Money 2.0
Projeto de desenvolvimento web, desenvolvido com Flask e jQuery.

## Utilizando o sistema

Python: 3.10.7

```sh
pip install -r requirements.txt
py run.py
```

## Exemplos de utilização com curl

#### Login - POST

curl <host>:5000/login -X POST -H "Content-Type: application/json" --data '{ "email":"lemuelkaue@gmail.com", "senha":"123"}'

#### Minha conta - GET

curl <host>/minha-conta -H "X-CSRF-TOKEN: <seu_token_gerado_por_login>"
