#!/bin/bash
# prerequisite installation script

[ $(id -u) -ne 0 ] && echo "run as root." && exit

SYSTEM_PKGS=(
  python-pip
  postgresql
  postgresql-server-dev-all
)

apt-get -y install "${SYSTEM_PKGS[@]}"
pip install -r requirements.txt
