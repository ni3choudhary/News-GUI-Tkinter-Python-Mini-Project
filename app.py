import io
import os
import webbrowser
import requests
from tkinter import Tk, Label, Frame, Button, BOTH, LEFT, DISABLED
from urllib.request import urlopen
from PIL import ImageTk,Image

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class NewsGui:
    
    def __init__(self) -> None:
        # url for location india
        url = "https://newsapi.org/v2/top-headlines?country=in&apiKey={}".format(os.environ['API_KEY'])
        # fetch data
        self.data = requests.get(url).json()

        # Load GUI
        self.load_gui()

        # load the 1st news item
        self.load_news_item(0)
    
    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0,0)
        self.root.title('News GUI Python')
        self.root.configure(background='black')

    def clear(self):
        for slaves in self.root.pack_slaves():
            slaves.destroy()

    def load_news_item(self,index):

        # clear the screen for the new news item
        self.clear()

        # set news image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_image_data = urlopen(img_url).read()
            img = Image.open(io.BytesIO(raw_image_data)).resize((350,250))
            image = ImageTk.PhotoImage(img)
        except:
            img_url = 'https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found-300x169.jpg'
            raw_image_data = urlopen(img_url).read()
            img = Image.open(io.BytesIO(raw_image_data)).resize((350, 250))
            image = ImageTk.PhotoImage(img)

        label = Label(self.root,image=image)
        label.pack()


        news_headline = Label(self.root,text=self.data['articles'][index]['title'],bg='black',fg='white',wraplength=350,justify='center')
        news_headline.pack(pady=(10,20))
        news_headline.config(font=('verdana',15))

        news_desc = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350,justify='center')
        news_desc.pack(pady=(2, 20))
        news_desc.config(font=('verdana', 12))

        frame = Frame(self.root,bg='black')
        frame.pack(expand=True,fill=BOTH)

        # PREV BUTTON
        if index != 0:
            prev = Button(frame,text='Prev', cursor = 'hand2',width=16,height=3,command=lambda :self.load_news_item(index-1))
            prev.pack(side=LEFT)
        else:
            prev = Button(frame,text='Prev', state = DISABLED,width=16,height=3)
            prev.pack(side=LEFT)

        # READMORE BUTTON
        read = Button(frame, text='Read More', cursor = 'hand2',width=16, height=3,command=lambda :self.open_link(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        # NEXT BUTTON
        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', cursor = 'hand2',width=16, height=3,command=lambda :self.load_news_item(index+1))
            next.pack(side=LEFT)
        else:
            next = Button(frame, text='Next', state= DISABLED ,width=16, height=3)
            next.pack(side=LEFT)

        self.root.mainloop()

    # Open link in browser if clicked on read more button
    def open_link(self,url):
        webbrowser.open(url)


news = NewsGui()