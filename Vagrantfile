# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.communicator = "ssh"
  config.ssh.username = "ubuntu"
  config.ssh.insert_key = true

  config.vm.network "forwarded_port", guest: 5432, host: 5432   # postgresql
  config.vm.network "forwarded_port", guest: 8080, host: 8080   # http

  config.vm.provider "virtualbox" do |vb|
    vb.name = "pasta"
    vb.memory = "512"
    vb.cpus = "1"
    vb.gui = false
  end

  config.vm.provision "shell",
    inline: "sudo apt-get -y install aptitude python"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "vagrant.yml"
    ansible.verbose = false
    ansible.sudo = true
  end

  config.vm.synced_folder ".", "/vagrant"
end
