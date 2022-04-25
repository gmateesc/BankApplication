mkdir -p /tmp/Banking/accounts/

cd app
export FLASK_APP=bank_app

#python3 -m flask run
python3 ${FLASK_APP}.py


