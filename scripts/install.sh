#!/bin/bash
[ $(id -u) -ne 0 ] && echo "run as root." && exit

SYSTEM_PKGS=(
  postgresql
  postgresql-client
  postgresql-server-all
  virtualenv
)

apt install "${SYSTEM_PKGS[@]}"

cd ..

[ ! -d venv ] && virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

cd -
