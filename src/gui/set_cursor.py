def set_cursor(widget, cursor):
    # Recursively set all the children's cursor to a given cursor value
    for child in widget.winfo_children():
        set_cursor(widget=child, cursor=cursor)
        
    widget.config(cursor=cursor)