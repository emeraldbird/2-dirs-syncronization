#!/usr/bin/python3
"""

The script performs a one-way synchronization of two folders

"""

from argparse import ArgumentParser, RawTextHelpFormatter
from stat import ST_MODE, ST_UID, ST_GID
from shutil import copy2, copytree, rmtree, copystat, chown
from shutil import SpecialFileError
from time import sleep
from typing import Tuple
import filecmp
import os
import sys
import logging
import signal


#logging.basicConfig(level=logging.INFO)

class Syncronizer():
    """
    One-way syncronization of two folders

    Example:
        sync = Syncronizer('./master_dir/', './slave_dir/', interval=1.5, log_file='./sync.log')
        sync.run()

    """
    def __init__(self,
                 master: str,
                 slave: str,
                 interval: float = 1.0,
                 log_level: int = logging.INFO,
                 log_file: str = ''):

        self.master = os.path.abspath(master)
        self.slave = os.path.abspath(slave)
        self.interval = interval
        self.running = False

        self.__setup_logger(level=log_level, log_file=log_file)

    def run(self) -> None:
        """
        Run syncronization
        """
        self.running = True

        self.logger.info('Start syncronization %s ----> %s', self.master, self.slave)

        while self.running:
            self.syncronize()
            sleep(self.interval)

        self.logger.info('Stop syncronization %s --X--> %s', self.master, self.slave)

    def stop(self) -> None:
        """
        Can be used in signal handler:
            signal.signal(signal.SIG_INT, labmda _sig_no, _stack_frame: syncronizer_object.stop())
        """
        self.running = False

    def syncronize(self) -> None:
        """
        Syncronize two folders once
        """
        self.remove()
        self.update()
        self.distribute()

    def remove(self) -> None:
        """
        Remove outdated files from slave directory
        """
        for path_in_slave, _, type_ in self.__get_unique(self.slave, self.master):
            if type_ == 'dir':
                rmtree(self.__verify(path_in_slave))
                #log
                self.logger.info('removed: dir %s', path_in_slave)

            elif type_ == 'file':
                os.remove(self.__verify(path_in_slave))
                #log
                self.logger.info('removed: file %s', path_in_slave)

    def update(self) -> None:
        """
        Replace all files in slave directory whose type/size/modification time has changed
        Update stat, UID, GID
        """
        def __sync_stats(path_in_master, path_in_slave):
            stat_in_master = os.stat(path_in_master)
            stat_in_slave = os.stat(path_in_slave)

            if stat_in_master[ST_MODE] != stat_in_slave[ST_MODE]:
                copystat(path_in_master, path_in_slave)
                # log
                self.logger.info('changed stat: %s', path_in_slave)

            if stat_in_master[ST_UID] != stat_in_slave[ST_UID]:
                chown(path=path_in_slave, user=stat_in_master[ST_UID])
                # log
                self.logger.info('changed UID: %s', path_in_slave)

            if stat_in_master[ST_GID] != stat_in_slave[ST_GID]:
                chown(path=path_in_slave, group=stat_in_master[ST_GID])
                # log
                self.logger.info('changed GID: %s', path_in_slave)

        for dirpath, directories, filenames in os.walk(self.slave):

            for dirname in directories:

                path_in_master, path_in_slave = self.__m_s_paths(dirpath, dirname)

                if not os.path.exists(path_in_master):
                    continue

                __sync_stats(path_in_master, path_in_slave)

            for filename in filenames:

                path_in_master, path_in_slave = self.__m_s_paths(dirpath, filename)

                if not os.path.exists(path_in_master):
                    continue

                __sync_stats(path_in_master, path_in_slave)

                if not filecmp.cmp(path_in_master, path_in_slave):
                    copy2(path_in_master, path_in_slave)
                    # log
                    self.logger.info('updated: %s', path_in_slave)

    def distribute(self) -> None:
        """
        Copy new files from master to slave
        """
        for path_in_master, path_in_slave, type_ in self.__get_unique(self.master, self.slave):
            try:
                if type_ == 'dir':
                    copytree(path_in_master, path_in_slave)
                    # log
                    self.logger.info('copied: dir %s', path_in_slave)

                elif type_ == 'file':
                    copy2(path_in_master, path_in_slave)
                    #log
                    self.logger.info('copied: file %s', path_in_slave)

            except SpecialFileError:
                self.logger.error('copy failed: %s', path_in_slave)

    def __m_s_paths(self, dirpath, name) -> Tuple[str, str]:
        relative_path = os.path.relpath(
            path=os.path.join(dirpath, name),
            start=self.slave)
        path_in_master = os.path.join(self.master, relative_path)
        path_in_slave = os.path.join(self.slave, relative_path)

        return (path_in_master, path_in_slave)

    def __get_unique(self, original_dir: str, comparison_dir: str) -> Tuple[str, str, str]:
        """
        Generator returns relative path of file in original_dir that absent in comparison_dir.
        Also we could use filecmp.dircmp instead, but there is an issue to handle subdirectories.
        """
        for dirpath, directories, filenames in os.walk(original_dir):

            for directory in directories:

                relative_path = os.path.relpath(
                    path=os.path.join(dirpath, directory),
                    start=original_dir)

                cheking_dir = os.path.join(comparison_dir, relative_path)

                if not os.path.exists(cheking_dir):
                    directory_path = os.path.join(dirpath, directory)

                    yield (directory_path, cheking_dir, 'dir')

            for filename in filenames:
                relative_path = os.path.relpath(
                    path=os.path.join(dirpath, filename),
                    start=original_dir)

                cheking_file = os.path.join(comparison_dir, relative_path)

                if not os.path.exists(cheking_file):
                    filepath = os.path.join(dirpath, filename)

                    yield (filepath, cheking_file, 'file')

    def __verify(self, path_: str) -> str:
        """
        If ok - return str, if not - raise Exception
        """
        # check if path_ is inside master or inside slave
        abspath_ = os.path.abspath(path_)

        if os.path.commonpath((self.master, abspath_)) == self.master \
            or os.path.commonpath((self.slave, abspath_)) == self.slave:

            return path_

        else:
            raise Exception(f'file {abspath_} not in {self.master} or {self.slave}')

    def __setup_logger(self, level: int, log_file: str = ''):
        self.logger = logging.getLogger(f'{sys.argv[0]} PID {os.getpid()}')
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            '%(asctime)s : %(name)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        s_handler = logging.StreamHandler()
        s_handler.setLevel(level)
        s_handler.setFormatter(formatter)

        if log_file:
            f_handler = logging.FileHandler(log_file)
            f_handler.setLevel(level)
            f_handler.setFormatter(formatter)
            self.logger.addHandler(f_handler)

        self.logger.propagate = False       # fix duplicates

        self.logger.addHandler(s_handler)


def main():
    """
    main
    """
    parser = ArgumentParser()
    parser = ArgumentParser(
        description=(f"(Linux version)\nThe script starts one-way syncronization between 2 folders"
                     f"Example: {sys.argv[0]} -i 0.1 --log-file sync.log ./master/ ./slave/"),
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('master', type=str)
    parser.add_argument('slave', type=str)
    parser.add_argument('--interval', '-i', default=1.0, type=float)
    parser.add_argument('--log-file', type=str)

    args = parser.parse_args()

    syncronizer = Syncronizer( \
            args.master, \
            args.slave, \
            interval=args.interval, \
            log_file=args.log_file \
            )

    signal.signal(signal.SIGINT, lambda _sig_no, _stack_frame: syncronizer.stop())

    syncronizer.run()

if __name__ == '__main__':
    main()
