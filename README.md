# BankApplication

Bank application with A REST API


1. [Install the web application](#install)
   1. [Update pip](#update_pip)
   2. [Install dependencies for Flask application](#install_deps)


2. [Start the web application](#start)


3. [Build the Docker image](#build_image)
   1. [Create the Dockerfile](#dockerfile)
   2. [Build the docker image](#image)
   3. [Run the web application as a container](#run_image)



4. [Use the web application](#access_api)
   1. [Create a bank account](#create_account)
   2. [Get the bank accounts](#get_account)




<a name="install" id="install"></a>
## Install the web application


<a name="update_pip" id="update_pip"></a>
### Update pip

Run
```bash
  $ python3 -m pip install --upgrade pip
```

then check

```bash
  $ pip3 --version
  pip 22.0.4 from /usr/local/lib/python3.9/site-packages/pip (python 3.9)
```





<a name="install_deps" id="install_deps"></a>
### Install dependencies for Flask application


Run
```
  $ cd BankApplication/WebApp

  $ more  dependencies/requirements.txt 
  Flask>=0.12.2
  six>=1.10.0
  virtualenv>=15.1.0


  $ pip3 install -r  dependencies/requirements.txt
  ...
```







<a name="start" id="start"></a>
## Start the web application



Use this start script:
```
  $ cd BankApplication/WebApp

  $ more start.sh 
  mkdir -p /tmp/Banking/accounts/

  cd app
  export FLASK_APP=banking_bank

  python3 ${FLASK_APP}.py
```



Run the start script:
```
  $ cd BankApplication/WebApp

  $ ./start.sh
   * Serving Flask app 'banking_bank' (lazy loading)
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
  
```






<a name="build_image" id="build_image"></a>
## Build the Docker image


<a name="dockerfile" id="dockerfile"></a>
### Create the Dockerfile

```bash
  $ cd BankApplication

  $ more Dockerfile 
  FROM ubuntu:20.04

  WORKDIR /tmp/Banking
  COPY BankApplication .

  RUN apt-get update  -y && \
      apt-get install -y python3 python3-pip && \
      pip3 install    -r dependencies/requirements.txt 

  ENV DEBUG=True
  EXPOSE 5000

  CMD [ "bash", "-c", "cd /tmp/Banking && ./start.sh" ]
```




<a name="image" id="image"></a>
### Build the docker image

```bash
  $ cd BankApplication
  
  $ docker build -t app:latest .
  [+] Building 134.2s (10/10) FINISHED
  ...
  Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them


  $ docker image ls
  REPOSITORY                TAG       IMAGE ID       CREATED         SIZE
  app                       latest    43e90a338097   6 minutes ago   454MB
```






<a name="run_image" id="run_image"></a>
### Run the web application as a container


```bash

  $ docker run -d -p 5000:5000 app
  33ae2a6c3e81da037aef9cb5da9c1fa7498e33ea0748e86fd144ac14a9775e0e

  $ docker ps
  CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS        PORTS                    NAMES
  33ae2a6c3e81   app     "bash -c 'cd /tmp/Ba…"   5 seconds ago   Up 3 seconds  0.0.0.0:5000->5000/tcp   serene_bouman
```







<a name="access_api" id="access_api"></a>
## Use the web application


<a name="create_account" id="create_account"></a>
### Create a bank account


Define the payload of the REST API request in a file
```bash 

  $ cd BankApplication/WebApp
  
  $ more payload.json
  {
      "iban": "CH13 1234 5678 9012 3456 0",
      "type": "checking",
      "customer_id": 3399        
  }
```


Send request to the API

```
  $ cd BankApplication/WebApp

  $ curl -sS \
               -X POST -d @payload.json  \
               -H 'Content-Type: application/json'  \
	       http://127.0.0.1:5000/banking/api/v1/accounts
  {
    "currency": "", 
    "customer_id": 3399, 
    "iban": "CH13 1234 5678 9012 3456 0", 
    "id": "2", 
    "type": "checking"
  }
```






<a name="get_account" id="get_account"></a>
### Get the bank accounts


Get all accounts
```bash
  $ curl -sS    -H 'Content-Type: application/json'  http://127.0.0.1:8888/banking/api/v1/accounts
  {
    "accounts": [
      {
        "currency": "", 
        "customer_id": 3399, 
        "iban": "CH13 1234 5678 9012 3456 0", 
        "id": "2", 
        "type": "checking"
      }
    ]
  }
```



Get a specific account
```bash
  $ curl -sS  -H 'Content-Type: application/json'  http://127.0.0.1:5000/banking/api/v1/accounts/2
  {
    "accounts": [
      {
        "currency": "", 
        "customer_id": 3399, 
        "iban": "CH13 1234 5678 9012 3456 0", 
        "id": "2", 
        "type": "checking"
      }
    ]
  }
```

