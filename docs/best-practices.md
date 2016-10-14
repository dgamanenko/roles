## Best practices for writing Ansible roles

The aim of this repository is to provide a home for Ansible roles with the following properties:

- Reusable
- Provide sane defaults
- Flexible & extensible


### Scope

Roles should be narrow in scope. They should focus on configuring a specific piece of software or aspect of the system.
For example, a role for Nginx should install Nginx, generate configuration files, and manage the Nginx service. The
role should *not* make assumptions about what types of applications Nginx should be serving, like UWSGI vs. CGI.
Instead, the role should provide reasonable defaults and allow settings to be overridden for various levels of
customization.


### Defaults

Roles should provide reasonable defaults that either accomodate the most common use cases, or reflect the existing
defaults of the component being configured. Users should generally be able to run a role and end up with a reasonably
configured system without having to override many variables.

As an example, the `logstash` role in this repo contains filters and patterns for collecting logs from several common
pieces of open source software, including Nginx, Elasticsearch, and PostgreSQL. These files are installed on the target
server by default, making it easy to collect logs from these components without much configuration. Even though these
filters are installed by default, they don't interfere with other software on the system and can be explicitly excluded
if the user doesn't need the filters.


### Flexibility

While roles should provide reasonable defaults for most settings, users should be able to override settings. As
mentioned in the previous section, the `logstash` role provides many filters and patterns by default. However, the role
also exposes variables that allow users to specify their own filter and pattern files to be copied to the target.

In general, any time a role creates a configuration file on the target using the `copy` or `template` module, the file
or template used should be overridable. For example, an `nginx` role should provide a default template for `nginx.conf`
in its `templates` directory. In addition, the role should provide a variable (e.g. `nginx_config_path`) so that users
can provide their own custom template file. This flexibility allows for greater reusability, since users are free to
provide a completely custom configuration file tailored to their application and are not restricted by the role's
default template.


### Dependencies

Ansible provides a mechanism for specifying [dependencies][ansible-dependencies] on other roles. Dependencies should be
used to extend the functionality of a role, similar to inheritance or composition in object oriented programming.
Suppose your application uses Nginx and you're using a general-purpose `nginx` role that that someone else has written.
The role generally suits your needs, but you'd like to set the size of the TCP buffer (via
`net.ipv4.tcp_max_syn_backlog`) to improve performance. A reasonable approach would be to extend the `nginx` role by
creating a new role and adding a dependency on the `nginx` role. Then, you can add a task in your sub-role that
configures the size of the TCP buffer.

Role dependencies should *not* be thought of in the sense of package dependencies. Logstash, for example, requires Java
to be installed. To ensure that Java is installed before installing Logstash, you could write a `java` role and a
`logstash` role and add a dependency from the `logstash` role to the `java` role. However, this is a poor idea for
multiple reasons. First, it introduces coupling and reduces reusability. There are several implementations of Java;
what if the `java` role installs OracleJDK, but you want to use OpenJDK? Second, a role's dependencies are run before
the role itself is run. If you only want to update Logstash configuration files, there is no reason to run the `java`
role first.

### Tagging

For complex applications, playbooks may include many roles. Unless a new server is being configured from scratch,
it's often unnecessary to run the entire playbook. Fortunately, [tags][ansible-tags] can be used to run a subset of
tasks.

Each task in a role should include one or more tags. The first tag should be the name of the role that the task is a
part of. Additional subtags should be used to group tasks within a role that are commonly run together, such as
installation, configuration, and service management. For example, a task in an `nginx` role that installs Nginx should
include tags like `nginx` and `nginx:install`:

    - name: Install nginx
      apt: name=nginx state=present
      tags: ['nginx', 'nginx:install']

A task in the same role that generates configuration files should include tags like `nginx` and `nginx:configuration`:

    - name: Copy nginx.conf
      template: src=nginx.conf dest=/etc/nginx/nginx.conf
      notify: restart nginx
      tags: ['nginx', 'nginx:configuration']

Rather than tagging each task individually, you can instead apply tags to multiple tasks when including files. Assume
an `nginx` role has the following structure:

    nginx
    ├── defaults
    │   └── main.yml
    ├── tasks
    │   ├── configuration.yml
    │   ├── install.yml
    │   └── main.yml
    └── templates
        └── nginx.conf

If `configuration.yml` contains tasks related to configuration and `install.yml` contains tasks related to
installation, you could include these files and apply tags in `main.yml`:

    ---

    - include: install.yml
      tags: ['nginx', 'nginx:install']

    - include: configuration.yml
      tags: ['nginx', 'nginx:configuration']


[ansible-dependencies]: https://docs.ansible.com/ansible/playbooks_roles.html#role-dependencies
[ansible-tags]: https://docs.ansible.com/ansible/playbooks_tags.html
