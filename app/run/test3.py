from tkinter import *
from tkinter import ttk

root_window = Tk()

estyle = ttk.Style()
# estyle.element_create("plain.field", "from", "clam")
# estyle.layout("EntryStyle.TEntry",
#                    [('Entry.plain.field', {'children': [(
#                        'Entry.background', {'children': [(
#                            'Entry.padding', {'children': [(
#                                'Entry.textarea', {'sticky': 'nswe'})],
#                       'sticky': 'nswe'})], 'sticky': 'nswe'})],
#                       'border':'2', 'sticky': 'nswe'})])
# estyle.configure("EntryStyle.TEntry",
#                  background="green",
#                  foreground="black",
#                  fieldbackground="red")
# entry_v = StringVar()
# entry = ttk.Entry(root_window, style="EntryStyle.TEntry", textvariable=entry_v)
# entry.pack(padx=10, pady=10)


# estyle.element_create("plain.field", "from", "clam")
test = estyle.layout('TEntry')
print(test)
estyle.layout("custom.TEntry",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],'border':'2', 'sticky': 'nswe'})])
estyle.configure("custom.TEntry",
                 foreground="white",
                 fieldbackground="red")

estyle2 = ttk.Style()
estyle2.configure("custom2.TEntry",
                 foreground="black",
                 highlightcolor="red")
entry_v = StringVar()
entry = ttk.Entry(root_window, style="custom.TEntry", textvariable=entry_v)
entry2 = ttk.Entry(root_window, style="custom2.TEntry", textvariable=entry_v)
entry.pack(padx=10, pady=10)
entry2.pack(padx=20, pady=20)



root_window.mainloop()
