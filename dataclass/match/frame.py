from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.event import Event, Event
from dataclass.match.participant_frame import ParticipantFrame, ParticipantFrame


class Frame(BaseModel):
    events: List[Event] = Field(default_factory=list)
    participantFrames: Dict[str, ParticipantFrame] = Field(default_factory=dict)
    timestamp: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Frame":
        data['events'] = [Event.from_dict(v).to_dict() for v in data['events']]
        data['participantFrames'] = [ParticipantFrame.from_dict(v).to_dict() for v in data['participantFrames'].values()]

        return Frame(**data)
