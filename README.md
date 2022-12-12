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

curl <host>/minha-conta -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzgyOTU5MSwianRpIjoiYTU1MDFjN2UtOTE3ZC00ZWZkLWIyZDYtZTEyM2IwOTliNmY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY3ODI5NTkxLCJleHAiOjE2NjgwODg3OTF9.VNcB0rXBsCi50KZEq4Xu-v-80aXC3FC4fayTNE_OLRA" -H "Content-Type: application/json"