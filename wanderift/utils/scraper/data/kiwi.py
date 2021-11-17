import typing
import dataclasses


@dataclasses.dataclass
class Route:
    airline: str
    local_arrival: str
    local_departure: str
    utc_departure: str
    utc_arrival: str
    flight_no: int
    cityFrom: str
    cityTo: str
    flyFrom: str
    flyTo: str
    Return: int

    def json(self):
        return {
            "airline": self.airline,
            "local_departure": self.local_departure,
            "local_arrival": self.local_arrival,
            "utc_departure": self.utc_departure,
            "utc_arrival": self.utc_arrival,
            "flight_no": self.flight_no,
            "cityFrom": self.cityFrom,
            "cityTo": self.cityTo,
            "flyFrom": self.flyFrom,
            "flyTo": self.flyTo,
            "return": self.Return,
        }


@dataclasses.dataclass
class Flight:
    price: float
    route: typing.List[Route]
    local_departure: str
    local_arrival: str
    utc_departure: str
    utc_arrival: str
    cityFrom: str
    cityTo: str
    duration: typing.Dict[str, int]
    nightsInDest: int
    availability: int
    roundtrip: bool
    airlines: typing.List[str]
    deeplink: typing.Optional[str] = None


    def json(self):
        return {
            "price": self.price,
            "route": [o.json() for o in self.route],
            "local_departure": self.local_departure,
            "local_arrival": self.local_arrival,
            "utc_departure": self.utc_departure,
            "utc_arrival": self.utc_arrival,
            "cityFrom": self.cityFrom,
            "cityTo": self.cityTo,
            "duration": self.duration,
            "nightsInDest": self.nightsInDest,
            "availability": self.availability,
            "roundtrip": self.roundtrip,
            "airlines": self.airlines,
            "deeplink": self.deeplink
        }
