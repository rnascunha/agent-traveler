from pydantic import BaseModel


def dump_data(type: BaseModel, *, indent: int = 1):
    dump = type.model_json_schema()
    data = []
    for k, v in dump["properties"].items():
        data.append(" " * indent + f"{k}: {v["description"]}")

    return ",\n".join(data)
