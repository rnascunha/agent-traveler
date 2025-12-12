import copy
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
    if pp:
        new_highlight = copy.deepcopy(pp)
        new_highlight["photos"] = new_highlight["photos"][:1]
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
    if dd:
        # for f in ["address", "map_url", "latitude", "longitude", "photos", "types"]:
        for f in ["address", "map_url", "photos"]:
            if f != "photos":
                dest[f] = dd[f]
            else:
                dest[f] = dd[f][:1]
    else:
        logging.warning(f"Destination not found [{dest["name"]}]")
        logging.debug(dest)

    new_highlights = []
    for h in dest["highlights"]:
        new_highlights.append(update_highlight(h, dest, places))
    dest["highlights"] = new_highlights


def merge_data(state):
    destinations = copy.deepcopy(state.get("destination_data", []))
    places = state["places_data"]

    for dest in destinations:
        update_destination(dest, places)

    return destinations
