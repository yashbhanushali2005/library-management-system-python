from utils.file_handler import FileHandler

MEMBERS_FILE = "data/members.json"

class MemberService:
    def get_all(self):
        return FileHandler.read(MEMBERS_FILE)

    def add(self, name):
        members = self.get_all()
        members.append({
            "id": len(members) + 1,
            "name": name
        })
        FileHandler.write(MEMBERS_FILE, members)
