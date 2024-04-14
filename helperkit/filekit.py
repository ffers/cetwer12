import json, os


class FileKit:
    def load_file_json(self, unpay_order):
        try:
            with open(unpay_order, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found")
            return set()

    def save_file_json(self, file_json, data):
        with open(file_json, "w") as file:
            print("Записуєм в файл")
            json.dump(data, file)

    def search_data_in_files(self, directory, filename):  # Проходим по всем файлам в каталоге
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.endswith('.json'):
            return filepath
        else:
            return None


    def directory_load_json(self, path, flag=0):
        dataSave = {"CityList": []}
        try:
            files = os.listdir(path)  # откриваєм папку словарей городов
            files.sort()
            count = 0
            for filename in files:  # перебираем файли
                # print(filename)
                filepath = self.search_data_in_files(path, filename)  # первий файл
                if filepath:  # если найден
                    json_data = self.load_file_json(filepath)
                    if "City" in json_data:
                        dataSave["CityList"].extend(json_data["City"])


            return dataSave
        except FileNotFoundError:
            print("File not found")
            return set()