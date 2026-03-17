import importlib
import pkgutil

TRANSLATIONS = {}


def load_translations():
    for _, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + "."):
        if is_pkg:
            continue

        module = importlib.import_module(module_name)

        for attr_name in dir(module):
            if attr_name.isupper():
                section_dict = getattr(module, attr_name)

                if not isinstance(section_dict, dict):
                    continue

                TRANSLATIONS.setdefault(attr_name, {})
                TRANSLATIONS[attr_name].update(section_dict)


load_translations()
