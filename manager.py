
class NotEnoughDataException(Exception):
    pass


class NotEnoughMoneyException(Exception):
    pass


class NotEnoughStockException(Exception):
    pass


class NoActionException(Exception):
    pass


class Manager:
    def __init__(self, reader):
        self.reader = reader
        self.history = []
        self.account = 0
        self.stock = {}
        self.actions = {}

    def modify_account(self, value):
        if self.account + value < 0:
            raise NotEnoughMoneyException()
        self.account += value

    def add_history(self, row):
        self.history.append(row)

    def modify_stock(self, item, qty):
        if item not in self.stock:
            self.stock[item] = 0
        if self.stock[item] + qty < 0:
            raise NotEnoughStockException()
        self.stock[item] += qty

    def action(self, name, parameters):
        def action_in(callback):
            self.actions[name] = (parameters, callback)
        return action_in

    def process_action(self, action, rows):
        parameters, callback = self.actions[action]
        if len(rows) != parameters:
            raise NoActionException
        if callback(self, rows):
            self.add_history([action] + rows)

    def process(self):
        while True:
            action = self.reader.get_line()[0]
            if action == 'stop':
                break
            if action not in self.actions:
                raise NoActionException()
            parameters, callback = self.actions[action]
            rows = self.reader.get_line(parameters)
            self.process_action(action, rows)

    def review(self, start, end):
        return self.history[int(start):int(end)]

    def save(self):
        self.reader.write_history(self.history)


class FileHandler:
    def __init__(self, path):
        self.path_file = path
        self.file = open(path)

    def get_line(self, count=1):
        count_list = []
        for i in range(count):
            read_line = self.file.readline()
            if not read_line:
                raise NotEnoughDataException("za malo danych w pliku")
            count_list.append(read_line.strip())
        return count_list

    def write_history(self, history):
        self.file.close()
        with open("in.txt", "w") as f:
            for row in history:
                f.write("\n".join(row) + "\n")
            f.write("stop")
        self.file = open(self.path_file)
