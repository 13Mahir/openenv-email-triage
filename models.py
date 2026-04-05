from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, List, Optional

class Email(BaseModel):
    id: str
    sender: str
    subject: str
    body: str

class Observation(BaseModel):
    model_config = ConfigDict(extra='allow')
    inbox: List[Email]
    assigned_labels: Dict[str, str] = {}
    archived_emails: List[str] = []
    replied_emails: Dict[str, str] = {}
    available_actions: List[str]

class Action(BaseModel):
    model_config = ConfigDict(extra='allow')
    action_type: str
    email_id: Optional[str] = None
    label: Optional[str] = None
    reply_text: Optional[str] = None
