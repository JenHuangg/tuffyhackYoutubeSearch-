import tkinter
import tkinter.messagebox
from youtube import Search

NUMBER_OF_VID = 10
_FONT =  ('Open Sans', 11)

class YoutubeSearch:
    def __init__(self):
        self._root_window = tkinter.Tk()
        self._root_window.title('Youtube Search')
        self._root_window.configure(bg = 'thistle1')
        #self._root_window.geometry("900x600")
        #self._root_window.minsize(width = 450, height = 300)


        search_label = tkinter.Label(
            master = self._root_window,
            text = 'Search Results',
            font = ('open Sans', 14, 'bold' ),
            bg = 'thistle1')
        search_label.grid(
            row = 0, column = 0,
            columnspan = 7,
            sticky = tkinter.N + tkinter.E + tkinter.W)
        
        
        self._search_results = tkinter.Listbox(
            master = self._root_window,
            bg = 'thistle1',
            width = 100,
            height = 20,
            font = ('open sans', 13))
        self._search_results.bind(
            '<<ListboxSelect>>', self._show_more)
        self._search_results.grid(
            row = 1, column = 0,
            columnspan = 7,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._search_entry = tkinter.Entry(
            master = self._root_window, width = 20,
            bg = 'thistle3',
            font = _FONT)
        self._search_entry.grid(
            row = 3, column = 0,
            columnspan = 5,
            sticky = tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        search_button = tkinter.Button(
            master = self._root_window,
            text = 'Search',
            command = self._search,
            font = _FONT)
        search_button.grid(
            row = 3, column = 5,
            columnspan = 1,
            sticky = tkinter.W + tkinter.E)

        self._button_frame = tkinter.Frame(
            master = self._root_window)
        self._channel = self._create_check_button(
            'Channel', 2, 6)
        self._description = self._create_check_button(
            'Video Description', 3, 6)
        self._published_date = self._create_check_button(
            'Published Date', 4, 6)
        self._views = self._create_check_button(
            'Views', 5, 6)
        self._likes = self._create_check_button(
            'Likes', 6, 6)
        self._dislikes = self._create_check_button(
            'Dislikes', 7, 6)
        self._duration = self._create_check_button(
            'Duration', 8, 6)
        
        
        
        
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 2)
        
            
    

    def _search(self) -> None:
        to_search = self._search_entry.get()
        if to_search:
            self._search = Search(to_search)
            self._display_results()

            self._more_info_options = {
                self._channel: ['Channel: {}',
                                self._search.get_channel_title],
                self._description: ['Description: {}',
                                    self._search.get_description],
                self._published_date: ['Published Date: {}',
                                       self._search.get_published_date],
                self._views: ['Views: {}',
                              self._search.get_view_count],
                self._likes: ['Likes: {}',
                              self._search.get_liked_count],
                self._dislikes: ['Dislikes: {}',
                                 self._search.get_disliked_count],
                self._duration: ['Duration: {}',
                                 self._search.get_duration]}
            self._enable_buttons()
    

    def _display_results(self)-> None:
        self._search_results.delete('0', 'end')
        for video in range(NUMBER_OF_VID):
            self._search_results.insert(
                video,
                '{}.{}'.format(video + 1,
                               self._search.get_video_title(video + 1)))
    def _show_more(self, event):
        try:
            to_show_info = self._check_buttons()
            
            to_show = self._search_results.curselection()[0] + 1
            more_info_window = tkinter.Toplevel(
                master = self._root_window)
            
            more_info_window.title(self._search.get_video_title(to_show))
            #more_info_window.minsize(200,150)
            

            text = tkinter.Text(
                master = more_info_window,
                spacing3 = 6, width = 100,
                wrap = tkinter.WORD,
                font = ('open sans', 13),
                bg = 'thistle2')
            

            for option in to_show_info:
                text.insert(tkinter.END, '{}\n'.format(
                    to_show_info[option][0].format(
                       to_show_info[option][1](to_show))))
            text.pack()
        except:
            pass
    def _check_buttons(self) -> dict:
        checked = self._more_info_options.copy()
        
        return checked
    
    def _construct_more(self, video_num: int) -> str:
        message = ''
        message = 'Video Title: {}'.format(
            self._search.get_video_title(video_num))

        return message
    def _create_check_button(self, text, row, column) -> tkinter.Button:
        button = tkinter.Checkbutton(
            master = self._root_window,
            text = text,
            state = tkinter.DISABLED,
            bg = 'thistle1',
            font = _FONT,
            fg = 'black')
        button.grid(
            row = row, column = column,
            sticky = tkinter.W + tkinter.S + tkinter.N,
            )
        return button
    def _button_on(self, button: tkinter.Button):
        pass
    def _enable_buttons(self):
        for button in self._more_info_options:
            button['state'] = tkinter.NORMAL
        
    def run(self) -> None:
        self._root_window.mainloop()

if __name__ == '__main__':
    YoutubeSearch().run()
