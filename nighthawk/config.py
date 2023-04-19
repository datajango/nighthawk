import configparser
import json
import os

class Config:
    def __init__(self, filename, properties):
        self.filename = filename
        self.properties = properties
        self.config = None
        
        # Determine the file type
        if filename.lower().endswith('.ini'):
            self.file_type = 'ini'
            self.config = configparser.ConfigParser()
        else:
            self.file_type = 'json'
            self.config = {}

        self.load()

    def read(self):
        self.config.read(self.config_file)

    def write(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        
    def get(self, section, key, default=None):
        if self.file_type == 'ini':
            if not self.config.has_section(section):
                return default
            return self.config.get(section, key, fallback=default)
        elif self.file_type == 'json':
            return self.config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        if self.file_type == 'ini':
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, key, value)
        elif self.file_type == 'json':
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value

        self.save()

    def load(self):
        if self.file_type == 'ini':
            self.load_ini()
        else:
            self.load_json()

    def save(self):
        if self.file_type == 'ini':
            self.save_ini()
        else:
            self.save_json()

    def load_ini(self):
        self.config.read(self.filename)

        for prop in self.properties:
            section = prop['section']
            key = prop['key']
            default_value = prop['default_value']
            value = self.config.get(section, key, fallback=default_value)
            prop['value'] = value

    def load_json(self):
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, 'r') as f:
            data = json.load(f)

        for prop in self.properties:
            section = prop['section']
            key = prop['key']
            default_value = prop['default_value']
            value = data.get(section, {}).get(key, default_value)
            prop['value'] = value

    def save_ini(self):
        for prop in self.properties:
            section = prop['section']
            key = prop['key']
            value = str(prop['value'])  # Convert value to string for INI files

            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, key, value)

        with open(self.filename, 'w') as f:
            self.config.write(f)

    def save_json(self):
        data = {}

        for prop in self.properties:
            section = prop['section']
            key = prop['key']
            value = prop['value']

            if section not in data:
                data[section] = {}
            data[section][key] = value

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    