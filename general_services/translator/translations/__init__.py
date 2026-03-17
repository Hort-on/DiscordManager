import importlib
import pkgutil

TRANSLATIONS = {}


def merge_dicts(base: dict, new: dict):
    for section, values in new.items():
        base.setdefault(section, {}).update(values)


def load_translations():
    for _, module_name, is_pkg in pkgutil.walk_packages(__path__, __name__ + '.'):
        if is_pkg:
            continue

        module = importlib.import_module(module_name)

        for lang in ('en', 'uk'):
            lang_dict = getattr(module, lang, None)
            if not lang_dict:
                continue

            TRANSLATIONS.setdefault(lang, {})
            merge_dicts(TRANSLATIONS[lang], lang_dict)


load_translations()
