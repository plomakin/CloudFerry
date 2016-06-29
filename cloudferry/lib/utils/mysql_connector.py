# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.

import time

import sqlalchemy

from cloudferry.lib.utils import remote_runner

ALL_DATABASES = "--all-databases"


def get_db_host(cloud_config):
    """Returns DB host based on configuration.

    Useful when MySQL is deployed on multiple nodes, when multiple MySQL nodes
    are hidden behind a VIP. In this scenario providing VIP in
    `config.dst_mysql.db_host` will break mysqldump which requires to be run
    locally on particular DB host.

    :returns: `config.migrate.mysqldump_host` if not `None`, or
    `config.dst_mysql.db_host` otherwise
    """

    db_host = cloud_config.mysql.db_host

    if cloud_config.migrate.mysqldump_host:
        db_host = cloud_config.migrate.mysqldump_host

    return db_host


def dump_db(cloud, database=ALL_DATABASES):
    cmd = "mysqldump {database} --user={user}"
    if cloud.cloud_config.mysql.db_password:
        cmd += " --password={password}"

    db_host = get_db_host(cloud.cloud_config)
    rr = remote_runner.RemoteRunner(
        db_host, cloud.cloud_config.cloud.ssh_user,
        password=cloud.cloud_config.cloud.ssh_sudo_password)
    dump = rr.run(cmd,
                  database=database,
                  user=cloud.cloud_config.mysql.db_user,
                  password=cloud.cloud_config.mysql.db_password)

    filename = cloud.cloud_config.migrate.db_dump_filename
    with open(filename.format(database=('all_databases'
                                        if database == ALL_DATABASES
                                        else database),
                              time=time.time(),
                              position=cloud.position), 'w') as f:
        f.write(dump)


class MysqlConnector(object):
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.connection_url = self.compose_connection_url()

    def compose_connection_url(self):
        return '{}://{}:{}@{}:{}/{}'.format(self.config['db_connection'],
                                            self.config['db_user'],
                                            self.config['db_password'],
                                            self.config['db_host'],
                                            self.config['db_port'],
                                            self.db)

    def get_engine(self):
        return sqlalchemy.create_engine(self.connection_url)

    def execute(self, command, **kwargs):
        with sqlalchemy.create_engine(
                self.connection_url).begin() as connection:
            return connection.execute(sqlalchemy.text(command), **kwargs)

    def batch_execute(self, commands, **kwargs):
        with sqlalchemy.create_engine(
                self.connection_url).begin() as connection:
            for command in commands:
                connection.execute(sqlalchemy.text(command), **kwargs)
