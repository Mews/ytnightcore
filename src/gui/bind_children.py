def bind_children(widget, sequence, callback):
    for child in widget.winfo_children():
        bind_children(widget=child, sequence=sequence, callback=callback)
    
    return widget.bind(sequence, callback)