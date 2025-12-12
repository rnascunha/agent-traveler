import logging


def find(places, cond):
    for p in places:
        pp = cond(p)
        if pp:
            return p
    return None


def update_highlight(highlight_name, dest, places):
    pp = find(
        places,
        lambda place: dest["reference"] == place["reference"]
        and place["name"] == highlight_name
        and place["type"] == "highlights",
    )
    new_highlight = {}
    if pp:
        for f in ["name", "address", "map_url", "type"]:
            new_highlight[f] = pp[f]
        new_highlight["photos"] = pp["photos"][:1]
        return new_highlight
    else:
        logging.warning(f"Destination highlight not found [{highlight_name}]")
        return highlight_name


def update_destination(dest, places):
    dd = find(
        places,
        lambda place: place["type"] == "city"
        and place["reference"] == dest["reference"],
    )

    new_destination = {
        "name": dest["name"],
        "country": dest["country"],
        "brief": dest["brief"],
        "highlights": [],
    }
    if dd:
        for f in ["address", "map_url", "type"]:
            dest[f] = dd[f]
        dest[f] = dd[f][:1]
    else:
        logging.warning(f"Destination not found [{dest["name"]}]")
        logging.debug(dest)

    for h in dest["highlights"]:
        new_destination["highlights"].append(update_highlight(h, dest, places))

    return new_destination


def merge_data(state):
    destinations = state.get("destination_data", [])
    places = state["places_data"]

    new_destinations = []
    for dest in destinations:
        new_destinations.append(update_destination(dest, places))

    return new_destinations
