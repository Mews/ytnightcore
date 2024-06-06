from configparser import ConfigParser

def reset_default_configs():
    config = ConfigParser(allow_no_value=True)

    config.add_section("theme")
    config.set("theme", "; Available themes: https://ttkbootstrap.readthedocs.io/en/latest/themes/")
    config.set("theme", "theme", "darkly")

    with open("settings.ini", "w", encoding="utf-8") as f:
        config.write(f)

config = ConfigParser(allow_no_value=True)
config.read("settings.ini", encoding="utf-8")

theme = config.get("theme", "theme")