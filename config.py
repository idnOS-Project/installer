import toml
import os

CONFIG_FOLDER = "./config"

def list_variants() -> [str]:
    result = []
    for item in os.listdir(CONFIG_FOLDER + "/variants"):
        split = os.path.splitext(item)

        if os.path.isfile(f"{CONFIG_FOLDER}/variants/{item}") and split[-1].lower() == ".toml":
            result.append(split[0])

    return result

def load_config(variant=None) -> dict:
    def _load_config(rel_path):
        with open(CONFIG_FOLDER + "/" + rel_path + ".toml", "r") as f:
            return toml.load(f)

    base_config = _load_config("base")

    if variant is not None:
        merger = ConfigMerger(base_config)
        merger.merge(_load_config("variants/" + variant))
        return merger.config

    return base_config

class ConfigMerger:
    def __init__(self, initial_value=None):
        self.config = initial_value

    def merge(self, other_config):
        self.config = ConfigMerger.merge_config(self.config, other_config)

    # merges two dictionaries/objects with some special actions
    #
    # adding the minus `-` on an "incoming merge object" list will result in the
    # source object's item getting removed
    @staticmethod
    def merge_config(source, other) -> dict:
        def merge_list(source, other):
            for item in other:
                # items that has a `-` before it means to remove the item from the merge source
                if not item.startswith("-") and not item in source:
                    source.append(item)
                elif item.startswith("-"):
                    source.remove(item[1:])

            return source

        for key in other:
            other_item = other[key]
            source_item = source[key]

            if isinstance(other_item, list):
                source[key] = merge_list(source_item, other_item)
            else:
                source[key] = other_item

        return source

# list variants for debugging when not imported as a module
if __name__ == "__main__":
    from pprint import pprint

    print("Config variants:\n")
    print("base variant\n===")
    print(pprint(load_config()))
    print()

    for variant in list_variants():
        print(f"{variant} variant\n===")
        print(pprint(load_config(variant)))
        print()
