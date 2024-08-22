import enum

class ScopeClass(enum.Enum):
    user = "user"
    origin = "origin"
    
class StatusClass(enum.Enum):
    success = "SUCCESS"
    origin = "ORIGIN"
    processed = "PROCCESSED"
    deleted = "DELETED"
    failure = "FAILURE"
    pending = "PENDING"

class FaceTypeClass(enum.Enum):
    mosaic = "mosaic"
    character = "character"

class SchemaName(enum.Enum):
    user = "user"
    mzRequest = "mzRequest"
    mzResult = "mzResult"
    video = "video"
