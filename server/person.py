class Person:
    def __init__(self, client_address, name, client):
        self.client_address = client_address
        self.client = client
        self.name = None

    def set_name(self, name):
        self.name = name

    def __repr__(self):
        return f"Person({self.client_address}, {self.name})"