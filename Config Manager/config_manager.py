import os
import json
import yaml
import shutil
import datetime

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.read_config()
        if self.config_data:
            self.backup_config()
    
    def read_config(self):
        """
        Reads the configuration file and returns its content as a dictionary.
        Supports JSON and YAML formats.
        """
        try:
            with open(self.config_path, 'r') as file:
                if self.config_path.endswith('.json'):
                    return json.load(file)
                elif self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    return yaml.safe_load(file)
                else:
                    raise ValueError("Unsupported file format")
        except FileNotFoundError:
            print(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError:
            print("Error decoding JSON configuration file.")
        except yaml.YAMLError:
            print("Error decoding YAML configuration file.")
        except Exception as e:
            print(f"Error reading configuration file: {e}")
        return None
    
    def write_config(self, config_data):
        """
        Writes the given configuration data to the configuration file.
        Supports JSON and YAML formats.
        """
        try:
            with open(self.config_path, 'w') as file:
                if self.config_path.endswith('.json'):
                    json.dump(config_data, file, indent=4)
                elif self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(config_data, file, default_flow_style=False)
                else:
                    raise ValueError("Unsupported file format")
        except Exception as e:
            print(f"Error writing to configuration file: {e}")

    def backup_config(self):
        """
        Backs up the existing configuration file to a timestamped directory.
        Creates the backup directory if it does not exist.
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            backup_dir = f"backup_{timestamp}"
            backup_dir = "Config Manager/backups/" + backup_dir
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            shutil.copy(self.config_path, backup_dir)
            print(f"Backup created at {backup_dir}")
        except FileNotFoundError:
            print(f"Configuration file not found for backup: {self.config_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def validate_config(self):
        """
        Validates the configuration file to ensure it is in proper JSON or YAML format.
        Returns True if the configuration is valid, otherwise False.
        """
        try:
            if self.config_data is None:
                return False
            if isinstance(self.config_data, dict):
                print("Configuration file is valid.")
                return True
            else:
                print("Configuration file is not in the proper format.")
                return False
        except Exception as e:
            print(f"Error validating configuration file: {e}")
            return False

    def update_value(self, keys, new_value):
        """
        Updates the value in the configuration file based on the given keys.
        Supports nested structures.
        """
        def recursive_update(data, keys, value):
            if isinstance(data, dict):
                key = keys[0]
                if len(keys) == 1:
                    if key in data:
                        data[key] = value
                        return True
                    else:
                        print(f"Key '{key}' not found in the configuration.")
                        return False
                else:
                    if key in data and isinstance(data[key], dict):
                        return recursive_update(data[key], keys[1:], value)
                    else:
                        print(f"Key '{key}' not found or is not a dictionary.")
                        return False
            return False
        
        try:
            if self.config_data:
                if recursive_update(self.config_data, keys, new_value):
                    self.write_config(self.config_data)
                    print(f"Value updated successfully.")
                else:
                    print("Failed to update value in the configuration file.")
            else:
                print("Failed to read configuration file for update.")
        except Exception as e:
            print(f"Error updating value in configuration file: {e}")

class DevConfig(ConfigManager):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.env = 'development'

    def specific_method(self):
        """
        Development-specific method implementation.
        """
        print("Development-specific method.")

class StagingConfig(ConfigManager):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.env = 'staging'

    def specific_method(self):
        """
        Staging-specific method implementation.
        """
        print("Staging-specific method.")

class ProdConfig(ConfigManager):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.env = 'production'

    def specific_method(self):
        """
        Production-specific method implementation.
        """
        print("Production-specific method.")

# Example usage:
if __name__ == "__main__":
    dev_config = DevConfig("Config Manager/configs/dev_config.json")
    staging_config = StagingConfig("Config Manager/configs/staging_config.yaml")
    prod_config = ProdConfig("Config Manager/configs/prod_config.json")

    # Validate configurations
    is_valid = dev_config.validate_config()
    print(f"Config is valid: {is_valid}")

    # Update value
    dev_config.update_value(['database', 'port'], 1111)
