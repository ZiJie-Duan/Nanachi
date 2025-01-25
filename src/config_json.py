import json
import os

class Config:
    """
    This class provides a configuration file reader that combines JSON and environment variables.
    It allows reading configuration values from a local JSON file and environment variables.
    Environment variables should be in uppercase, such as "OPENAI_API_KEY_ACC3".
    
    example:
    {
        "OPENAI" : {
                "API" : "pj-xxxxxxxx",
                "PROJ" : {
                        "ACC" : "123123132"
                    }
            }
    }
    you can search by
        "OPENAI_API"
        "OPENAI_PROJ_ACC"
    """

    def __init__(self, file="config.json") -> None:
        self.file_exist = False
        self.data = None
        self.file = file
        self.load()
    
    def __call__(self, key) -> str:
        return self.get(key)
    
    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                    self.file_exist = True
            except:
                raise Exception("Failed to load JSON file")
    

    def json_search(self, key:str):
        key = key.split("_")
        res = self.json_recursive_search(self.data, key)
        if not res:
            raise Exception(f"Key '{'_'.join(key)}' not found in JSON file and environment")
        return res

    def json_recursive_search(self, node:any, key:any):
        # if node is leaf node but still have key
        if not isinstance(node, dict) and key:            
            return None
        # if node not leaf node but no key any more
        if isinstance(node, dict) and not key:
            return None
        # matched 
        if not isinstance(node, dict) and not key:
            return node 

        key_ac = None

        # Iterate through the keys
        for i, k in enumerate(key):
            if not key_ac:
                key_ac = k
            else:
                key_ac += "_" + k
            # Check if the accumulated key exists in the current node
            if key_ac in node:
                return self.json_recursive_search(
                    node[key_ac], key[i+1:])
        
        return None
    
    def get(self, key):
        value = os.getenv(key)
        if value is not None:
            return value
    
        if not self.file_exist:
            raise Exception(f"Configuration file does not exist and key '{key}' does not exist in environment")

        return self.json_search(key) 