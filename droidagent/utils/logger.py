import logging
import os

from ..config import agent_config

class Logger:
    def __init__(self, module_name):
        self.module_name = module_name
        self.initialized = False
        if agent_config.agent_output_dir is not None:
            self.initialize(module_name)

    def initialize_if_needed(self):
        if not self.initialized and agent_config.agent_output_dir is not None:
            self.initialize(self.module_name)

    def initialize(self, module_name):
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        
        if not os.path.exists(os.path.join(agent_config.agent_output_dir, 'logs')):
            os.makedirs(os.path.join(agent_config.agent_output_dir, 'logs'))
        
        file_handler = logging.FileHandler(os.path.join(agent_config.agent_output_dir, 'logs', f'agent_run.log'), mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s - %(asctime)s: %(message)s'))
        self.logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(name)s:%(levelname)s - %(message)s'))
        self.logger.addHandler(stream_handler)
        
        self.initialized = True

    def debug(self, msg):
        self.initialize_if_needed()
        if self.initialized:
            self.logger.debug(msg)
        else:
            print(f"DEBUG - {self.module_name}: {msg}")

    def info(self, msg):
        self.initialize_if_needed()
        if self.initialized:
            self.logger.info(msg)
        else:
            print(f"INFO - {self.module_name}: {msg}")

    def warning(self, msg):
        self.initialize_if_needed()
        if self.initialized:
            self.logger.warning(msg)
        else:
            print(f"WARNING - {self.module_name}: {msg}")

    def error(self, msg):
        self.initialize_if_needed()
        if self.initialized:
            self.logger.error(msg)
        else:
            print(f"ERROR - {self.module_name}: {msg}")
