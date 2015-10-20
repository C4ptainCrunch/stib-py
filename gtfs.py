from stib import Network
from collections import defaultdict, namedtuple

network = Network()

stops = defaultdict(list)

GTFS_Stop = namedtuple("Stop", ["stop_id", "stop_name", "stop_lat", "stop_lon"])

for line in network.lines[:4]:
    for direction in (1, 2):
        directed_ine = line.cast(direction)
        for stop in directed_ine.stops:
            stops[stop.name].append(stop)

gstops = []

for i, (name, same_stops) in enumerate(stops.iteritems()):
    lat = lon = 0
    for s in same_stops:
        lat += s.gps['latitude']
        lon += s.gps['longitude']
    lat, lon = lat / len(same_stops), lon / len(same_stops)
    gstops.append(GTFS_Stop(stop_id=i, stop_name=name, stop_lat=lat, stop_lon=lon))

GTFS_Route = namedtuple("Route", ["route_id", "route_short_name", "route_type", "route_color", "route_text_color"])

groutes = []

gtfs_types = {
    "B": 3,
    "M": 1,
    "T": 0
}

for i, line in enumerate(network.lines):
    t = gtfs_types[line.type]
    groutes.append(GTFS_Route(route_id=i, route_short_name=line.id, route_type=t, route_color=line.colors['bg'], route_text_color=line.colors['fg']))

GTFS_Trip = namedtuple("Trip", ["route_id", "service_id", "trip_id", "trip_headsign", "direction_id"])

gtrips = []

for i, route in enumerate(groutes):
    service = "NOCTIS" if isinstance(route.route_short_name, str) and route.route_short_name.startswith("N") else "NORMAL"
    for j, direction in enumerate((0, 1)):
        stib_line = list(filter(lambda x: x.id == route.route_short_name, network.lines))[0]
        head = stib_line.terminuses[j + 1]
        gtrips.append(GTFS_Trip(route_id=route.route_id, service_id=service, trip_id=i * 2 + j, trip_headsign=head, direction_id=j))

