import datetime
import json
import urllib.parse
from time import sleep

import dateutil.parser
import pytz
import timezonefinder
import requests
from typing import List

from wanderift.utils.scraper.data.kiwi import Flight, Route
from wanderift.utils.scraper.data.skyscanner import (
    Place,
    Carrier,
    Segment,
    Leg,
    Itinerary,
    PlaceQueryResponse,
)


class ScraperError(Exception):
    pass


class ScraperMaxTryReached(ScraperError):
    pass


class Skyscanner:
    MAX_TRY = 3
    MAX_RESULTS = 3

    def __init__(self, origin, destination, start_date, return_date):
        self.origin = origin
        self.destination = destination
        self.start_date = start_date
        self.return_date = return_date
        self.dt_departure = dateutil.parser.parse(start_date)
        self.dt_return = dateutil.parser.parse(return_date)
        self.headers = {
            "X-Skyscanner-ChannelID": "website",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
        }

    def query_place(self, place, is_destination: bool):
        url = (
            f"https://www.skyscanner.net/g/autosuggest-flights/KZ/en-GB/{place.lower()}"
        )
        params = {
            "isDestination": str(is_destination).lower(),
            "enable_general_search_v2": "true",
        }
        counter = 0
        while True:
            counter += 1
            if counter == self.MAX_TRY:
                raise ScraperMaxTryReached()
            try:
                response = requests.get(url, params)
            except requests.exceptions.RequestException:
                sleep(5)
                continue
            else:
                result = []
                for data in response.json():
                    try:
                        result.append(PlaceQueryResponse.from_dict(data))
                    except TypeError:
                        pass
                return result

    def get_place_info(self, place, is_destination: bool):
        results = self.query_place(place, is_destination)
        exact_matches = [r for r in results if r.PlaceId == place.upper()]
        best_matches = [r for r in results if r.PlaceId.startswith(place.upper())]
        if best_matches:
            return best_matches[0]
        if exact_matches:
            return exact_matches[0]

    def query(self, origin: PlaceQueryResponse, destination: PlaceQueryResponse):
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "geo_schema": "skyscanner",
            "carrier_schema": "skyscanner",
            "response_include": "query;deeplink;segment;stats;fqs;pqs",
        }

        data = {
            "destination": origin.PlaceId,
            "origin": destination.PlaceId,
            "adults": 1,
            "cabin_class": "economy",
            "options": {
                "include_unpriced_itineraries": True,
                "include_mixed_booking_options": True,
            },
            "limit": "3",
            "sort_by": "cheapest",
            "prefer_directs": False,
            "market": "US",
            "locale": "en-US",
            "currency": "USD",
            "legs": [
                {
                    "origin": origin.PlaceId,
                    "destination": destination.PlaceId,
                    "date": self.start_date,
                    "return_date": self.return_date,
                    "add_alternative_origins": False,
                    "add_alternative_destinations": False,
                }
            ],
        }
        counter = 0
        while True:
            counter += 1
            if counter == self.MAX_TRY:
                raise ScraperMaxTryReached()
            try:
                response = requests.post(
                    "https://www.skyscanner.com/g/conductor/v1/fps3/search/",
                    headers={**self.headers, **headers},
                    params=params,
                    json=data,
                )
            except requests.exceptions.RequestException:
                sleep(5)
                continue
            data = response.json()
            if data:
                return data

    def parse(self, data):
        places = {}
        carriers = {}
        segments = {}
        legs = {}
        trips = []
        for pj in data["places"]:
            place = Place.from_dict(pj)
            places[place.id] = place
        for cj in data["carriers"]:
            carrier = Carrier.from_dict(cj)
            carriers[carrier.id] = carrier
        for sj in data["segments"]:
            segment = Segment.from_dict(sj)
            segment.origin_place = places[segment.origin_place_id]
            segment.destination_place = places[segment.destination_place_id]
            segment.marketing_carrier = carriers[segment.marketing_carrier_id]
            segment.operating_carrier = carriers[segment.operating_carrier_id]
            segments[segment.id] = segment
        for lj in data["legs"]:
            leg = Leg.from_dict(lj)
            leg.origin_place = places[leg.origin_place_id]
            leg.destination_place = places[leg.destination_place_id]
            leg.segments = [segments[sid] for sid in leg.segment_ids]
            leg.marketing_carriers = [
                carriers[mcid] for mcid in leg.marketing_carrier_ids
            ]
            leg.operating_carriers = [
                carriers[ocid] for ocid in leg.operating_carrier_ids
            ]
            leg.stops = [places[sid] for sids in leg.stop_ids for sid in sids]
            legs[leg.id] = leg
        for tj in data["itineraries"]:
            trip = Itinerary.from_dict(tj)
            trip.legs = [legs[lid] for lid in trip.leg_ids]
            candidates = [c for c in tj["pricing_options"] if "amount" in c["price"]]
            if not candidates:
                continue
            best_option = min(candidates, key=lambda x: x["price"]["amount"])
            trip.price = best_option["price"]["amount"]
            departure = self.dt_departure.strftime("%y%m%d")
            dreturn = self.dt_return.strftime("%y%m%d")
            params = {
                "adults": 1,
                "children": 0,
                "adultsv2": 1,
                "childrenv2": "",
                "infants": "0",
                "cabinclass": "economy",
                "rtn": 1,
                "preferdirects": "false",
                "outboundaltsenabled": "false",
                "inboundaltsenabled": "false",
                "ref": f"home#/details/{trip.id}",
            }
            query = urllib.parse.urlencode(params)
            trip.deeplink = f"https://skyscanner.com/transport/flights/{self.origin.lower()}/{self.destination.lower()}/{departure}/{dreturn}/?{query}"
            trips.append(trip)
        return trips

    def transform(
        self,
        trip: Itinerary,
        *,
        tz_origin: pytz.timezone,
        tz_destination: pytz.timezone,
    ):
        route: List[Route] = []
        timezones: List[pytz.timezone] = [tz_origin, tz_destination]
        for leg_index, leg in enumerate(trip.legs):
            tz: pytz.timezone = timezones[leg_index]
            utc_departure: datetime.datetime = (
                tz_origin.localize(
                    dateutil.parser.parse(leg.segments[0].departure)
                ).astimezone(pytz.utc)
            )
            utc_arrival = None
            last_local_arrival = None
            for segment in leg.segments:
                if utc_arrival and last_local_arrival:
                    utc_departure = utc_arrival + (
                        dateutil.parser.parse(segment.arrival) - last_local_arrival
                    )
                utc_arrival = utc_departure + datetime.timedelta(
                    minutes=segment.duration
                )
                route.append(
                    Route(
                        airline=segment.marketing_carrier.display_code,
                        local_arrival=f"{segment.arrival}Z",
                        local_departure=f"{segment.departure}Z",
                        utc_departure=utc_departure.isoformat().replace("+00:00", "Z"),
                        utc_arrival=utc_arrival.isoformat().replace("+00:00", "Z"),
                        flight_no=int(segment.marketing_flight_number),
                        cityFrom=segment.origin_place.name,
                        cityTo=segment.destination_place.name,
                        flyFrom=segment.origin_place.display_code,
                        flyTo=segment.destination_place.display_code,
                        Return=int(leg_index == 1),
                    )
                )
                last_local_arrival = dateutil.parser.parse(segment.arrival)

        departure_duration = trip.legs[0].duration
        return_duration = trip.legs[1].duration if len(trip.legs) > 1 else None
        return Flight(
            price=round(trip.price),
            route=route,
            local_departure=trip.legs[0].departure,
            local_arrival=trip.legs[0].arrival,
            utc_departure=route[0].utc_departure,
            utc_arrival=route[len(trip.legs[0].segments) - 1].utc_arrival,
            cityFrom=trip.legs[0].origin_place.name,
            cityTo=trip.legs[0].destination_place.name,
            duration={
                "departure": departure_duration * 60,
                "return": return_duration * 60,
            },
            nightsInDest=1,  # TODO: fix
            availability=0,
            roundtrip=len(trip.legs) > 1,
            airlines=list(set(r.airline for r in route)),
            deeplink=trip.deeplink,
        )

    def run(self):
        origin = self.get_place_info(self.origin, False)
        destination = self.get_place_info(self.destination, False)
        tf = timezonefinder.TimezoneFinder()
        olat, olng = origin.lat_lon()
        dlat, dlng = destination.lat_lon()
        tz_origin = pytz.timezone(tf.timezone_at(lng=olng, lat=olat))
        tz_destination = pytz.timezone(tf.timezone_at(lng=dlng, lat=dlat))
        data = self.query(origin, destination)
        trips = self.parse(data)
        trips.sort(key=lambda x: x.price)
        return [
            self.transform(t, tz_origin=tz_origin, tz_destination=tz_destination).json()
            for t in trips[: self.MAX_RESULTS]
        ]


def main():
    skyscanner = Skyscanner(
        origin="NYC",
        destination="LON",
        start_date="2020-02-28",
        return_date="2020-03-01",
    )
    print(json.dumps(skyscanner.run(), indent=4))


if __name__ == "__main__":
    main()
