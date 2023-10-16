
<!-- ABOUT THE PROJECT -->
## About The Project

Тестовое задание в Центр Программного Обеспечения (Тестовое задание Сервер (5))


## Built With

* [![Docker][docker.com]][Docker-url]
* [![MySQL][mysql.org]][mysql-url]
* [![Django][djangoproject.com]][Django-url]
* [![Python][Python.org]][Python-url]

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple example steps.

## Description of the task solution

#### 1) Реализовано RestFullApi на DRF через обычный rest_framework.authtoken

#### 2) Для RestFullApi на DRF реализована документация через swagger. Чтобы пройти авторизацию в swagger и отправлять запросы, нужно вставить не просто токен который пришел, а "Token e364d9dc84713555fb940c19f1896d8071bb2e3d", так как swagger не подставляет автоматически в заголовок Authorization слово token. 

Описания находятся по адресу:

- <http://127.0.0.1:8000/swagger/>

- <http://127.0.0.1:8000/redoc/>

#### 3) Та часть задания, которая на визуальном оформлении, для просмотра нужно перейти на стартовую страницу и следовать подсказкам:
   - <http://127.0.0.1:8000/>


## Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```bash
   git clone https://github.com/Arahit0gami/test_software_center.git
   ```
2. При первом запуске проекта рекомендую запустить скрипт, либо вы специалист и знаете какие команды необходимо вводить😉
   ```
   ./script.sh
   ```
   В конце выполнения скрипта необходимо будет ввести логин и пароль для admin пользователя.
   Если возникли ошибки во время выполнения скрипта, запустите повторно, либо запустите поочередно команды, что там написаны.


## Author
[Kuzmenko Nikita](https://github.com/Arahit0gami)

## P.S.
На заметку тем, кто будет смотреть это тестовое задание. 
Обратной связи от компании не поступало, поэтому я не знаю, насколько хорошо или плохо было выполнено задание.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[djangoproject.com]: https://img.shields.io/badge/Django-4.2.5-green?style=plastic&logo=Django
[Django-url]: https://www.djangoproject.com/
[Python.org]: https://img.shields.io/badge/Python-3.11.0-green?style=plastic&logo=python
[Python-url]: https://python.org
[mysql.org]: https://img.shields.io/badge/MySQL-latest-green?style=plastic&logo=MySQL
[mysql-url]: https://www.mysql.com/
[docker.com]: https://img.shields.io/badge/Docker--compose-3.8-green?style=plastic&logo=docker
[Docker-url]: https://docker.com

