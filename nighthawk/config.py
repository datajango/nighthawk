import configparser
import json
import os

class Config:
    def __init__(self, config_file, properties):
        self.config_file = config_file
        self.properties = properties
        self.config = configparser.ConfigParser()
        self.load()

    def read(self):
        self.config.read(self.config_file)

    def write(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, key, default=None):
        if not self.config.has_section(section):
            return default
        return self.config.get(section, key, fallback=default)

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.write()
        
    def load(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)

        for prop in self.properties:
            section = prop['section']
            key = prop['key']

            if not self.config.has_section(section):
                self.config.add_section(section)

            if not self.config.has_option(section, key):
                self.config.set(section, key, prop['default_value'])

            prop['value'] = self.config.get(section, key)

    def save(self):
        for prop in self.properties:
            section = prop['section']
            key = prop['key']
            value = prop['value']
            self.config.set(section, key, value)

        with open(self.config_file, 'w') as file:
            self.config.write(file)
