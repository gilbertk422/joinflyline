import dataclasses
import inspect

from typing import List, Optional


class MyDataClass:
    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclasses.dataclass
class Place(MyDataClass):
    id: int
    alt_id: str
    parent_id: int
    name: str
    type: str
    display_code: str


@dataclasses.dataclass
class Carrier(MyDataClass):
    id: int
    name: str
    alt_id: str
    display_code: str
    display_code_type: str


@dataclasses.dataclass
class Segment(MyDataClass):
    id: str
    origin_place_id: int
    destination_place_id: int
    arrival: str
    departure: str
    duration: int
    marketing_flight_number: str
    marketing_carrier_id: int
    operating_carrier_id: int
    mode: str
    origin_place: Optional[Place] = None
    destination_place: Optional[Place] = None
    marketing_carrier: Optional[Carrier] = None
    operating_carrier: Optional[Carrier] = None


@dataclasses.dataclass
class Leg(MyDataClass):
    id: str
    origin_place_id: int
    destination_place_id: int
    departure: str
    arrival: str
    segment_ids: List[str]
    duration: int
    stop_count: int
    marketing_carrier_ids: List[int]
    operating_carrier_ids: List[int]
    stop_ids: List[int]
    origin_place: Optional[Place] = None
    destination_place: Optional[Place] = None
    segments: List[Segment] = dataclasses.field(default_factory=list)
    marketing_carriers: List[Carrier] = dataclasses.field(default_factory=list)
    operating_carriers: List[Carrier] = dataclasses.field(default_factory=list)
    stops: List[Place] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Itinerary(MyDataClass):
    id: str
    leg_ids: List[str]
    price: float = 0
    deeplink: str = ""
    legs: List[Leg] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class PlaceQueryResponse(MyDataClass):
    PlaceId: str
    Location: str

    def lat_lon(self):
        return tuple(map(float, self.Location.split(',')))