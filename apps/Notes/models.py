from bson import ObjectId

class Note:
    def __init__(self, title, content, user_id, date_created, date_modified):
        self._id = ObjectId()
        self.title = title
        self.content = content
        self.user_id = user_id
        self.date_created = date_created
        self.date_modified = date_modified