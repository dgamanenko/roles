# Ansible Roles

The purpose of this repository is to collect general-purpose Ansible roles with a focus on sane defaults,
extensibility, and reusability.


## Getting started

Clone this repo:

    $ cd /path/to/extra/roles
    $ git clone git@github.com:appsembler/roles.git appsembler_roles

Add it to your `ansible.cfg`:

    [defaults]
    roles_path = /path/to/extra/roles/appsembler_roles


## Philosophy

Roles that live in this repo should be general enough to be reused across multiple applications. Please read the
[documentation on best practices][best-practices].


[best-practices]: https://github.com/appsembler/roles/tree/develop/docs/best-practices.md
