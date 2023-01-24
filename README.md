# Docker

----

## Starting with docker 

To build the docker image

```shell
docker build -t name:tag .
```

`-t or --tag` the syntax for the following to be the name and tag

`first:tag`

The <u>_**name**_</u> signifies the name of the docker image

The <u>**_tag_**</u> is the tag image it can be used to give version names

![image](https://i.imgur.com/i0RNJ5j.png)

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./src ./src

ENTRYPOINT ["bash"]
```

----

To create the container

```shell
docker run --name image_test_container -it name:tag
```

With this, after running this with the dockerfile, it will run the container with the name of `image_test_container`
from the image `name:tag`

![](https://i.imgur.com/XVc68zC.png)

---

typing `exit` will exit the docker

---

|    command     |                  description                  |
|:--------------:|:---------------------------------------------:|
|  `docker ps`   |       show all of the active container        |
| `docker ps -a` | show all of the active and inactive container |

---

## Running the python program

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]
```

----

```dockerfile
FROM python:3.11.0rc1

WORKDIR /code

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT ["python", "src/main.py"]
```

## installing pip

source ../docker_venv/bin/activate

```shell
source ../docker_venv/bin/activate
pip freeze > requirements.txt
```