from ttkbootstrap import Style

def get_color(color_code):
    colors = Style().colors

    for color_name in colors:
        if color_name == color_code:
            return colors.get(color_name)