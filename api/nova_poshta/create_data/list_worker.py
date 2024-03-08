import json

class ListClient():
    def load_processed(self, file_json):
        try:
            with open(file_json, "r") as file:
                return list(json.load(file))
        except FileNotFoundError:
            return list()

    def save_processed(self, file_json, processed):
        with open(file_json, "w") as file:
            json.dump(list(processed), file)

    def add_in_list(self, file_json, data):
        processed = self.load_processed(file_json)
        processed.append(data)
        self.save_processed(file_json, processed)
        return processed

    def remove_in_list(self, file_json):
        processed = self.load_processed(file_json)
        processed.clear()
        self.save_processed(file_json, processed)
        return processed
