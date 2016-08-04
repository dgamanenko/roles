#!/usr/bin/env python

import logging
import sys

import curator
import elasticsearch
import certifi

HOSTS = ["{{ logstash_output_elasticsearch_hosts | join('\", \"') }}"]
USERNAME = '{{ logstash_output_elasticsearch_user }}'
PASSWORD = '{{ logstash_output_elasticsearch_password }}'
DELETE_OLDER_THAN = {{ logstash_remove_older_than }}


def main():
    for host in HOSTS:
        scheme, _, domain = host.rpartition('://')
        scheme = scheme if scheme else 'http'
        basic_auth_uri = '{}://{}:{}@{}'.format(scheme, USERNAME, PASSWORD, domain)

        client = elasticsearch.Elasticsearch([basic_auth_uri], verify_certs=True,
                                             ca_certs=certifi.where())

        index_list = curator.IndexList(client)
        index_list.filter_by_regex(kind='prefix', value='logstash-')
        index_list.filter_by_age(source='name', direction='older',
                                 timestring='%Y.%m.%d', unit='days',
                                 unit_count=DELETE_OLDER_THAN)

        if len(index_list.indices):
            logging.info('Deleting indices: {}'
                         .format(', '.join(index_list.indices)))
            delete_indices = curator.DeleteIndices(index_list)
            delete_indices.do_action()
        else:
            logging.info('No indices to delete')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
