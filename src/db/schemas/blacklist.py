from pydantic import BaseModel


class Blacklist(BaseModel):
    pass

class BlacklistEmail(Blacklist):
    email: str
    app_uuid: str
    blocked_reason: str
    host_ip: str
    
class BlacklistReason(Blacklist):
    found: bool
    blocked_reason: str