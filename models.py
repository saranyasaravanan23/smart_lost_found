class User:
    def __init__(self, username, email, password, role="USER"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role


class Item:
    def __init__(self, user_id, item_name, category,
                 location, description, report_type):

        self.user_id = user_id
        self.item_name = item_name
        self.category = category
        self.location = location
        self.description = description
        self.report_type = report_type
        self.status = "OPEN"