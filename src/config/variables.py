import yaml
from dotenv import load_dotenv
import os


class ConfigVariables:
    def __init__(self, root):
        self.root = root
        self.list = self.parse_config_file()
        self.write_env_variables()

    def parse_config_file(self):
        try:
            with open(f'{self.root}config.yml', 'r') as ymlfile:
                cfg = yaml.safe_load(ymlfile)
            temp = cfg.copy()
            for key, val in cfg.items():
                if isinstance(val, dict):
                    for k, v in val.items():
                        temp[k] = v
            return temp
        except FileNotFoundError:
            print("Config file not found.")
            return {}
        except Exception as e:
            print(f"Failed to parse config file: {e}")
            return {}

    def write_env_variables(self):
        try:
            with open(f'{self.root}.env', 'w') as file:
                for element in self.list.get('env-variables', []):
                    for key, value in element.items():
                        file.write(f'{key.upper()}={value}\n')
        except FileNotFoundError:
            print("Environment file not found.")
        except Exception as e:
            print(f"Failed to write environment variables: {e}")

    def env_vars(self, *args):
        load_dotenv()
        return {arg: str(os.getenv(arg)) for arg in args}

    def __call__(self, *args):
        sub_dict = {}
        for arg in args:
            if arg in self.list:
                sub_dict[arg] = self.list[arg]
            else:
                print(f"Warning: '{arg}' not found in the configuration.")
        return sub_dict
