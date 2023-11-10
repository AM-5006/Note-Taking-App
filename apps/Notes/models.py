from bson import ObjectId

class Note:
    def __init__(self, title, content, user_id):
        self._id = ObjectId()
        self.title = title
        self.content = content
        self.user_id = user_id