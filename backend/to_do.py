import uuid

class To_do:
    # title = str()
    # desc = str()

    def __init__(self, title, desc, task_id):
        self.set_title(title)
        self.set_desc(desc)
        self.__id = str(task_id) if task_id is not None else str(uuid.uuid4())[:8]

    # def __init__(self, title, desc, *args):
    #     self.set_title(title)
    #     self.set_desc(desc)
    #     if len(args) == 1:
    #         self.__id = str(args[0])
    #     else:
    #         self.__id = str(uuid.uuid4())[:8]
        
    def get_id(self):
        return self.__id

    def get_title(self):
        return self.title

    def set_title(self, title):
        if type(title) != str:
            raise TypeError("Title must be a string")
        title = title.strip()
        if title == '':
            raise ValueError("Title cannot be empty")
        if len(title) > 30:
            raise ValueError("Title cannot exceed 30 characters")
        if title.isdigit():
            raise ValueError("Title cannot be only numerical")
        self.title = title

    def get_desc(self):
        return self.desc

    def set_desc(self, desc):
        if type(desc) != str:
            raise TypeError("Description must be a string")
        desc = desc.strip()
        if len(desc) > 200:
            raise ValueError("Description cannot exceed 200 characters")
        if desc.isdigit():
            raise ValueError("Description cannot be only numerical")
        self.desc = desc