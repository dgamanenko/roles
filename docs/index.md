## Installation

By default, Ansible looks for roles in the `roles` directory next to the playbook being run. You can also use the
[`roles_path`][roles-path] setting in your [`ansible.cfg`][ansible-cfg] to specify other directories where Ansible
should look for roles.


### Simple setup

Clone the repository:

    $ cd /path/to/extra/roles
    $ git clone git@github.com:appsembler/roles.git appsembler_roles

Now add a line in your `ansible.cfg` to tell Ansible where to find the roles:

    [defaults]
    roles_path = /path/to/extra/roles/appsembler_roles

You can now use the roles in your playbooks normally:

    ---

    - name: Run the sftp role from appsembler/roles
      hosts: all
      become: yes
      become_method: sudo
      roles:
        - sftp


### Using git submodules

If you have a git repo containing some playbooks and you want to use roles from this repo, you can use
[git submodules][git-submodules] to add this repo as a dependency. From your playbooks directory, run:

    $ git submodule add git@github.com:appsembler/roles.git appsembler_roles

Add the submodule directory to your `roles_path` in `ansible.cfg`:

    [defaults]
    roles_path = ./appsembler_roles


[ansible-cfg]: https://docs.ansible.com/ansible/intro_configuration.html
[roles-path]: https://docs.ansible.com/ansible/intro_configuration.html#roles-path
[git-submodules]: https://git-scm.com/docs/git-submodule
