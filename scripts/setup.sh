#!/bin/bash
# database setup script

[ $(id -u) -ne 0 ] && echo "[!] run as root." && exit

echo -n "Username: "
read owner

[ -z "$owner" ] && echo "[!] missing username." && exit

echo "creating database owner ..."
sudo -u postgres createuser "$owner" --interactive -P
[ $? -ne 0 ] && exit || echo "[+] user created: $owner"

echo "creating databases ..."
DATABASES=("app" "dev" "test")
for i in ${DATABASES[@]}; do
  sudo -u postgres createdb "$i" -O "$owner" && echo "[+] db created: $i";
done
