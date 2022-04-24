# BankApplication

Bank application with A REST API



## Update pip


Run
```bash
  $ python3 -m pip install --upgrade pip
```

then check

```bash
  $ pip3 --version
  pip 22.0.4 from /usr/local/lib/python3.9/site-packages/pip (python 3.9)
```




## Install dependencies for Flask application


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





## Start the application



Use this start script:
```
  $ cd BankApplication/WebApp

  $ more start.sh 
  mkdir -p /tmp/Abraxas/accounts/

  cd app
  export FLASK_APP=abraxas_bank

  python3 ${FLASK_APP}.py
```



Run the start script:
```
  $ cd BankApplication/WebApp

  $ ./start.sh
   * Serving Flask app 'abraxas_bank' (lazy loading)
   * Environment: production
     WARNING: This is a development server. Do not use it in a production deployment.
     Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
  
```





## Build the Docker image


### Create the Dockerfile

```bash
  $ cd BankApplication

  $ more Dockerfile 
  FROM ubuntu:20.04

  WORKDIR /tmp/Abraxas
  COPY BankApplication .

  RUN apt-get update  -y && \
      apt-get install -y python3 python3-pip && \
      pip3 install    -r dependencies/requirements.txt 

  ENV DEBUG=True
  EXPOSE 5000

  CMD [ "bash", "-c", "cd /tmp/Abraxas && ./start.sh" ]
```





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




### Run the web application as a container


```bash

  $ docker run -d -p 5000:5000 app
  33ae2a6c3e81da037aef9cb5da9c1fa7498e33ea0748e86fd144ac14a9775e0e

  $ docker ps
  CONTAINER ID   IMAGE   COMMAND                  CREATED         STATUS        PORTS                    NAMES
  33ae2a6c3e81   app     "bash -c 'cd /tmp/Ab…"   5 seconds ago   Up 3 seconds  0.0.0.0:5000->5000/tcp   serene_bouman
```




## Use the web application


### Create an account


Define the REST API pyaload in a file
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
	       http://127.0.0.1:5000/abraxas/api/v1/accounts
  {
    "currency": "", 
    "customer_id": 3399, 
    "iban": "CH13 1234 5678 9012 3456 0", 
    "id": "2", 
    "type": "checking"
  }
```





### Get the accounts



Get all accounts
```bash
  $ curl -sS    -H 'Content-Type: application/json'  http://127.0.0.1:8888/abraxas/api/v1/accounts
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
  $ curl -sS  -H 'Content-Type: application/json'  http://127.0.0.1:5000/abraxas/api/v1/accounts/2
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

