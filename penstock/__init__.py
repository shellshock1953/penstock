# -*- coding: utf-8 -*-
"""
Penstock (Coucdb Replication Manager)
"""
from gevent import monkey
monkey.patch_all()

import logging
from logging.config import dictConfig
import argparse
import gevent
import consul
from couchdb.client import Database, Server
from yaml import load
from time import sleep
import sys, os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

logger = logging.getLogger('replichecker')


def get_task_for_replication(server, replicator_document):
    for task in server.tasks():
        if task['type'] == 'replication' and task.get('doc_id', None) == replicator_document['_id']:
            logger.debug(repr(task))
            return task


def check_replication(server, replicator_document, configuration):
    sleep(5)
    replication_task = get_task_for_replication(server, replicator_document)
    while replication_task:
        logger.info("Current progress ({0[replication_id]}): {0[progress]}".format(replication_task))
        sleep(5)
        replication_task = get_task_for_replication(server, replicator_document)
    logger.info("No task for replication")


def create_replication(replicator_db, target, source):
    logger.info("Create replication.")
    replicator_document_id = replicator_db.create({
        'create_target':  True,
        'continuous': True,
        'target': target,
        'source': source
    })
    replicator_document = replicator_db[replicator_document_id]
    logger.info("Replication created ({})".format(str(replicator_document)))
    return replicator_document


def get_sources_list(configuration):
    if 'consul_sources' in configuration:
        consul_conf = configuration['consul_sources']
        c = consul.Consul()
        services = c.catalog.service(consul_conf['name'], tag=consul_conf.get('tag', None))[1]
        return set(["http://{1[user]}:{1[password]}@{0[Address]}:{0[ServicePort]}/{1[database]}".format(service, consul_conf)
                    for service in services])
    else:
        return set([source['url'] for source in configuration['sources']])


def run_checker(configuration):
    """
    """

    server = Server(configuration['admin'])
    replicator_db = server['_replicator']
    sources_list = get_sources_list(configuration)
    black_listed_sources = set([])
    while 1:
        replicator_document = None
        for replication_id in replicator_db:
            if not replication_id.startswith('_design/'):

                replicator_document_temp = replicator_db[replication_id]
                if replicator_document_temp['target'] != configuration['target'] and replicator_document_temp.get('continuous', False):
                    continue
                if replicator_document_temp['source'] not in sources_list:
                    continue
                if replicator_document_temp.get('_replication_state', '') != 'triggered':
                    logger.info("Delete replication. ID: {0[_id]}".format(replicator_document_temp))
                    black_listed_sources.add(replicator_document_temp['source'])
                    logger.info('Blacklisted: {}'.format(black_listed_sources))
                    replicator_db.delete(replicator_document_temp)
                replicator_document = replicator_document_temp
        if not replicator_document:
            # create replication
            logger.info("No active replication")
            white_listed_sources = sources_list - black_listed_sources
            if white_listed_sources:
                replicator_document = create_replication(replicator_db,
                                                         configuration['target'],
                                                         white_listed_sources.pop())
            else:
                logger.warning("No white listed sources")
                sleep(30)
                logger.warning("Start with all listed sources")
                black_listed_sources = set([])
                continue

        check_replication(server, replicator_document, configuration)
        logger.info("Wait replication.")
        sleep(10)


def main():
    parser = argparse.ArgumentParser(description='---- Penstock ----')
    parser.add_argument('config', type=str, help='Path to configuration file')
    params = parser.parse_args()
    logger.info("Start Penstock.")
    if os.path.isfile(params.config):
        with open(params.config) as config_file_obj:
            config = load(config_file_obj.read())
        dictConfig(config)
        replications = {}
        for replication_id in config:
            if replication_id.startswith('replication_'):
                logger.info("Start replication {}".format(replication_id))
                replications[replication_id] = gevent.spawn(run_checker, config[replication_id])
        while 1:
            for replication_id in replications:
                if replications[replication_id].ready():
                    sleep(10)
                    logger.info("Handle restart replication {}".format(replication_id))
                    replications[replication_id] = gevent.spawn(run_checker, config[replication_id])
            sleep(30)


##############################################################

if __name__ == "__main__":
    main()