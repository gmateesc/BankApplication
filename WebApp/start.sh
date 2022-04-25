mkdir -p /tmp/Abraxas/accounts/

cd app
export FLASK_APP=abraxas_bank

#python3 -m flask run
python3 ${FLASK_APP}.py


