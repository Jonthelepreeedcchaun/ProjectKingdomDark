class json_obj:
    def __init__(self, path = 'Storage/'):
        self.retrieve(path)
    def retrieve(self, path = 'Storage/'):
        import os, json
        for this in os.listdir(path):
            if this[-5:] == ".json":
                with open('Storage/' + this, 'r', encoding='utf-8') as f:
                    exec('self.' + this[:-5] + ' = json.load(f)')
    def save(self, attr):
        import json
        if hasattr(self, attr):
            with open('Storage/' + attr + '.json', 'w', encoding = 'utf-8') as f:
                exec('json.dump(self.' + attr + ', f, ensure_ascii = False, indent = 4)')
        else:
            raise Exception('Jsondata Error: ' + attr + '.json inaccessable')
