import configparser
import os

class ConfigLoader:
    def __init__(self, config_file='config/fix_settings.cfg'):
        """
        Initialize the config loader and load the configuration file.
        
        Args:
            config_file (str): The path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """
        Load the configuration from the specified file.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found.")
        self.config.read(self.config_file)

    def get(self, section, option, fallback=None):
        """
        Get a specific configuration value from the loaded config.

        Args:
            section (str): The section in the config file (e.g., 'SESSION').
            option (str): The specific option within the section (e.g., 'SocketConnectHost').
            fallback (Any): Default value to return if the option is not found.
        
        Returns:
            str: The configuration value or the fallback if not found.
        """
        return self.config.get(section, option, fallback=fallback)

    def get_int(self, section, option, fallback=0):
        """
        Get an integer value from the config.

        Args:
            section (str): The section in the config file.
            option (str): The option within the section.
            fallback (int): Default value to return if the option is not found.
        
        Returns:
            int: The configuration value as an integer.
        """
        return self.config.getint(section, option, fallback=fallback)

    def get_float(self, section, option, fallback=0.0):
        """
        Get a float value from the config.

        Args:
            section (str): The section in the config file.
            option (str): The option within the section.
            fallback (float): Default value to return if the option is not found.
        
        Returns:
            float: The configuration value as a float.
        """
        return self.config.getfloat(section, option, fallback=fallback)

    def get_boolean(self, section, option, fallback=False):
        """
        Get a boolean value from the config.

        Args:
            section (str): The section in the config file.
            option (str): The option within the section.
            fallback (bool): Default value to return if the option is not found.
        
        Returns:
            bool: The configuration value as a boolean.
        """
        return self.config.getboolean(section, option, fallback=fallback)
