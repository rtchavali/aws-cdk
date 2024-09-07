import os


class GlobalConfig:
    _instance = None  # For Singleton instance
    _config = {}

    def __new__(cls):
        """Create or return the single instance of the class."""
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
        return cls._instance


    def get_config(self):
        return self._config

    def update_config(self, path: str, value):
        keys = path.split(".")
        d = self._config
        for key in keys[:-1]:
            d = d.setdefault(key, {})  # Create nested dicts if they don't exist
        d[keys[-1]] = value

    def append_config(self, new_config):
        def merge_dicts(d1, d2):
            for key, value in d2.items():
                if isinstance(value, dict) and key in d1:
                    # If both values are dicts, merge them recursively
                    merge_dicts(d1[key], value)
                else:
                    # Otherwise, just set the value
                    d1[key] = value
        merge_dicts(self._config, new_config)

