from pydantic import BaseModel


def dump_data(type: BaseModel, *, indent: int = 1, exclude_keys: list[str] = []):
    """
    A helper function to create prompts based on pydanctic class.

    Output the key fields and its description.

    Args:
      type: the pydanctic type to output
      indent: how many indent output spaces

    Returns:
      String with formatted output
    """
    dump = type.model_json_schema()
    data = []
    for k, v in filter(lambda x: x[0] not in exclude_keys, dump["properties"].items()):
        data.append(" " * indent + f'"{k}": {v["description"]}')

    return ",\n".join(data)
