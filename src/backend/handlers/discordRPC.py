import time
from pypresence import Presence
from pypresence.types import ActivityType

class DiscordRPC:
    def __init__(self):
        self.clientID = "1320113441964429423"
        self.rpc = Presence(self.clientID)
        self.isConnected = False
        self.lastError = ""
    
    def connect(self):
        try:
            self.rpc.connect()
            self.isConnected = True
            self.lastError = ""
            return True
        except Exception as exc:
            self.isConnected = False
            self.lastError = str(exc)
            return False

    def update(self,
        title="ThisCordRPC",
        details="",
        state="",
        largeImage="",
        smallImage="",
        largeImageText="",
        smallImageText=""
    ):
        if not self.isConnected:
            return
        
        self.rpc.update(
            activity_type=ActivityType.PLAYING,
            name=title,
            details=details if details else None,
            state=state if state else None,
            large_image=largeImage if largeImage else None,
            small_image=smallImage if smallImage else None,
            large_text=largeImageText if largeImageText else None,
            small_text=smallImageText if smallImageText else None,
            start=int(time.time())
        )
    
    def clear(self):
        if self.isConnected:
            self.rpc.clear()
