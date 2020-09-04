import tkinter as tk
from tkinter import ttk

class CustomNotebook(ttk.Notebook):
    '''A ttk Notebook with close buttons on each tab'''
    def __init__(self, parent, *args, **kwargs):
        kwargs['style'] = 'CustomNotebook'
        self.__initialize_custom_style()
        ttk.Notebook.__init__(self, parent, *args, **kwargs)
        self._active = None
        self.bind('<ButtonPress-1>', self.close_btn_press, True)
        self.bind('<ButtonRelease-1>', self.close_btn_release)
        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.exit_)


    def enter(self, event):
        pass
        # print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))

    # function to be called when when mouse exits the frame
    def exit_(self, event):
        pass
        # print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))

    def close_btn_press(self, event):
        '''Called when the button is pressed over the close button'''

        element = self.identify(event.x, event.y)
        print(element)

        if 'close' in element:
            index = self.index('@%d,%d' % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def close_btn_release(self, event):
        '''Called when the button is released over the close button'''
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index('@%d,%d' % (event.x, event.y))

        if 'close' in element and self._active == index:
            self.forget(index)
            self.event_generate('<<NotebookTabClosed>>')

        self.state(['!pressed'])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage('img_close', data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage('img_closeactive', data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage('img_closepressed', data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create('close', 'image', 'img_close',
                            ('active', 'pressed', '!disabled', 'img_closepressed'),
                            ('active', '!disabled', 'img_closeactive'), border=10, sticky='e')
        style.configure('CustomNotebook', tabposition='ne')
        style.layout('CustomNotebook', [('CustomNotebook.client', {'sticky': ''})])
        style.layout('CustomNotebook.Tab', [
            ('CustomNotebook.tab', {
                #'side': 'right',
                'sticky': '',
                'children': [
                    ('CustomNotebook.padding', {
                        'side': 'top',
                        'sticky': '',
                        'children': [
                            ('CustomNotebook.focus',{
                                'side': 'top',
                                'sticky': '',
                                'children': [
                                    ('CustomNotebook.label', {'side': 'left', 'sticky': ''}),
                                    ('CustomNotebook.close', {'side': 'right', 'sticky': ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x100')
    notebook = CustomNotebook(root)
    notebook.place(relx=0, rely=0, relwidth=1, relheight=1)

    for color in ('red', 'orange', 'green', 'blue', 'violet'):
        frame = tk.Frame(notebook, background=color)
        notebook.add(frame, text=color)

    root.mainloop()
