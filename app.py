import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk,Image
from currency_api import mod_rates, base_rates
from freecurrencyapi import Client

class App(tk.Tk):
    api_key = "fca_live_yu7yQwc4SvkO7O63eDzsllyJk0ogRy20nWZfdV6T"
    client = Client(api_key)    
    
    bg_color = '#02111F'
    white = '#FFFFFF'
    black= '#000000'
    blue = '#22D3EE' # light blue
    dark_blue='#1D72BA' # currency # entry
    red = '#FF0000' #right-side
    dark_red="#E11414"
    violet = '#7F007F' #shared
    gray='#3C3C3C' # placeholder text

    def __init__(self):
        super().__init__()
        self.title('Currency Converter')
        self.geometry('1200x750')
        self['bg']=App.bg_color
        self.resizable(0,0)
        self.font=('Tahoma',16)
        self.bg_preset={'bg':App.bg_color}
        
        self.rounded_blue=self.resize("images/Rectangle 1.png",100,50)
        self.rounded_big_blue=self.resize('images/Rectangle 1.png',110,50)
        self.rounded_dark_blue=self.resize("images/Rectangle 2.png",100,50)
        self.rounded_red=self.resize("images/Rectangle 3.png",140,50)
        self.rounded_gray=self.resize("images/Rectangle 4.png",100,50)
        self.rounded_small_gray=self.resize("images/Rectangle 5.png",30,30)

        self.map_img=self.resize("images/Map.png",835,415)

        self.flags={
            "EUR":ImageTk.PhotoImage(file="images/Unknown.png"),"USD":ImageTk.PhotoImage(file="images/United-States.png"),"JPY":ImageTk.PhotoImage(file="images/Japan.png"),"BGN":ImageTk.PhotoImage(file="images/Bulgaria.png"),"CZK":ImageTk.PhotoImage(file="images/Czech-Republic.png"),"DKK":ImageTk.PhotoImage(file="images/Denmark.png"),"GBP":ImageTk.PhotoImage(file="images/United-Kingdom.png"),"HUF":ImageTk.PhotoImage(file="images/Hungary.png"),"PLN":ImageTk.PhotoImage(file="images/Poland.png"),"RON":ImageTk.PhotoImage(file="images/Romania.png"),"SEK":ImageTk.PhotoImage(file="images/Sweden.png"),"CHF":ImageTk.PhotoImage(file="images/Switzerland.png"),"ISK":ImageTk.PhotoImage(file="images/Iceland.png"),"NOK":ImageTk.PhotoImage(file="images/Norway.png"),"HRK":ImageTk.PhotoImage(file="images/Croatia.png"),"RUB":ImageTk.PhotoImage(file="images/Russia.png"),"TRY":ImageTk.PhotoImage(file="images/Turkey.png"),"AUD":ImageTk.PhotoImage(file="images/Australia.png"),"BRL":ImageTk.PhotoImage(file="images/Brazil.png"),"CAD":ImageTk.PhotoImage(file="images/Canada.png"),"CNY":ImageTk.PhotoImage(file="images/China.png"),"HKD":ImageTk.PhotoImage(file="images/Hong-Kong.png"),"IDR":ImageTk.PhotoImage(file="images/Indonesia.png"),"ILS":ImageTk.PhotoImage(file="images/Israel.png"),"INR":ImageTk.PhotoImage(file="images/India.png"),"KRW":ImageTk.PhotoImage(file="images/South-Korea.png"),"MXN":ImageTk.PhotoImage(file="images/Mexico.png"),"MYR":ImageTk.PhotoImage(file="images/Malaysia.png"),"NZD":ImageTk.PhotoImage(file="images/New-Zealand.png"),"PHP":ImageTk.PhotoImage(file="images/Philippines.png"),"SGD":ImageTk.PhotoImage(file="images/Singapore.png"),"THB":ImageTk.PhotoImage(file="images/Thailand.png"),"ZAR":ImageTk.PhotoImage(file="images/South-Africa.png"),"UNK":ImageTk.PhotoImage(file="images/Unknown.png")
                    }
        self.symbols={"EUR":"€","USD":"$","JPY":"¥","BGN":"лв","CZK":"Kč","DKK":"kr","GBP":"£","HUF":"Ft","PLN":"zł","RON":"lei","SEK":"kr","CHF":"Fr.","ISK":"kr","NOK":"kr","HRK":"kn","RUB":"₽","TRY":"₺","AUD":"A$","BRL":"R$","CAD":"C$","CNY":"CN¥","HKD":"HK$","IDR":"Rp","ILS":"₪","INR":"₹","KRW":"₩","MXN":"MX$","MYR":"RM","NZD":"NZ$","PHP":"₱","SGD":"S$","THB":"฿","ZAR":"R","UNK":"?"}
        
        self.title_one=tk.Label(self,**self.widget_preset(App.bg_color,App.blue,('Tahoma',20,'bold')),text='Currency')
        self.title_one.place(relx=.45,rely=.03,anchor='n')
        
        self.title_two=tk.Label(self,**self.widget_preset(App.bg_color,App.white,('Tahoma',20,'bold')),text='Converter')
        self.title_two.place(relx=.56,rely=.03,anchor='n')

        self.base_frame=tk.Frame(self, bg=App.bg_color)
        self.base_frame.place(relx=.138,rely=.147,relwidth=.133,relheight=.2)

        self.base_text=tk.Label(self.base_frame,**self.widget_preset(App.bg_color,App.blue),text='Base')
        self.base_text.place(relx=.531,relwidth=.306,relheight=.16)

        self.base_flag=tk.Label(self.base_frame,image=self.flags["EUR"],bg=App.bg_color)
        self.base_flag.place(rely=.233)

        self.base_curr_frame=tk.Frame(self.base_frame)
        self.base_curr_frame.place(relx=.375,rely=.233,relwidth=.625,relheight=.333)

        self.base_curr_container=tk.Label(self.base_curr_frame,image=self.rounded_blue)
        self.base_curr_container.place(relwidth=1,relheight=1)
        self.base_curr_input=tk.StringVar()
        self.base_curr_entry=tk.Entry(self.base_curr_container,**self.widget_preset(App.white,App.gray),borderwidth=0,highlightthickness=0,textvariable=self.base_curr_input)
        self.base_curr_entry.place(relwidth=1,relheight=1)

        self.base_curr_entry.insert(0,"USD..")
        self.base_curr_entry.bind("<FocusIn>",self.base_rm_curr)


        self.base_curr_symbol=tk.Label(self.base_frame,**self.widget_preset(App.bg_color,App.blue))
        self.base_curr_symbol.place(relx=.113,rely=.76)

        self.base_curr_input.trace_add('write',self.base_on_curr_input)

        self.base_amount_frame=tk.Frame(self.base_frame)
        self.base_amount_frame.place(relx=.375,rely=.667,relwidth=.625,relheight=.333)

        self.base_amount_container=tk.Label(self.base_amount_frame,image=self.rounded_dark_blue)
        self.base_amount_container.place(relwidth=1,relheight=1)
        
        self.base_amount_input=tk.StringVar()
        self.base_amount_entry=tk.Entry(self.base_amount_container,borderwidth=0,highlightthickness=0,**self.widget_preset(App.white,App.gray),textvariable=self.base_amount_input)
        self.base_amount_entry.place(relwidth=1,relheight=1)
        
        self.base_amount_entry.insert(0,"0..")
        
        self.base_amount_entry.bind("<FocusIn>",self.base_rm_amount)


        self.middle_arrow=tk.Label(self,**self.widget_preset(App.bg_color,App.white),text='->')
        self.middle_arrow.place(relx=.5,rely=.21,anchor='c')

        self.latest_frame=tk.Frame(self)
        self.latest_frame.place(relx=.5,rely=.3,anchor='c',relwidth=.092,relheight=.066)

        self.latest_container=tk.Label(self.latest_frame,image=self.rounded_big_blue)
        self.latest_container.place(relwidth=1,relheight=1)

        self.latest=tk.Button(self.latest_container,**self.widget_preset(App.black,App.white,('Tahoma',16,'bold')),border=0,activebackground=App.white,activeforeground=App.bg_color,text='Latest',command=self.get_latest)
        self.latest.place(relwidth=1,relheight=1)

        self.targ_frame=tk.Frame(self,bg=App.bg_color)
        self.targ_frame.place(relx=.725,rely=.147,relwidth=.167,relheight=.253)

        self.targ_text=tk.Label(self.targ_frame,**self.widget_preset(App.bg_color,App.red),text='Convert to')
        self.targ_text.place(relx=.375)

        self.targ_flag=tk.Label(self.targ_frame,image=self.flags["EUR"],bg=App.bg_color)
        self.targ_flag.place(rely=.175)

        self.targ_curr_frame=tk.Frame(self.targ_frame)
        self.targ_curr_frame.place(relx=.3,rely=.175,relwidth=.7,relheight=.25)

        self.targ_curr_container=tk.Label(self.targ_curr_frame,image=self.rounded_red)
        self.targ_curr_container.place(relwidth=1,relheight=1)

        self.targ_curr_input=tk.StringVar()
        self.targ_curr_entry=tk.Entry(self.targ_curr_container,borderwidth=0,highlightthickness=0,**self.widget_preset(App.white,App.gray),textvariable=self.targ_curr_input)
        self.targ_curr_entry.place(relwidth=1,relheight=1)
       
        self.targ_curr_entry.insert(0,"USD,CAD..")
        self.targ_curr_entry.bind("<FocusIn>",self.targ_rm_curr)
        self.targ_curr_symbol=tk.Label(self.targ_frame,**self.widget_preset(App.bg_color,App.red))
        self.targ_curr_symbol.place(relx=.09,rely=.57)

        self.targ_curr_input.trace_add("write",self.targ_on_curr_input)
        self.targ_amount_frame=tk.Frame(self.targ_frame)
        self.targ_amount_frame.place(relx=.3,rely=.5,relwidth=.5,relheight=.25)
        self.targ_amount_container=tk.Label(self.targ_amount_frame,image=self.rounded_gray)
        self.targ_amount_container.place(relwidth=1,relheight=1)

        self.targ_amount_value=tk.StringVar()
        
        self.targ_amount_entry=tk.Entry(self.targ_amount_container,**self.widget_preset(App.white,App.white),state="readonly",readonlybackground=App.dark_red,textvariable=self.targ_amount_value)
        self.targ_amount_entry.place(relwidth=1,relheight=1)
        self.base_amount_input.trace_add("write",self.base_on_amount_input)
        
        self.targ_back_frame=tk.Frame(self.targ_frame)
        self.targ_next_frame=tk.Frame(self.targ_frame)

        self.map_frame=tk.Frame(self)
        self.map_frame.place(relx=.153,rely=.44,relwidth=.696,relheight=.553)
        
        self.map=tk.Label(self.map_frame,image=self.map_img)
        self.map.place(relwidth=1,relheight=1)
        
        self.buttons=[self.targ_back_frame,self.targ_next_frame]
            
        self.valid_entries=self.flags.keys()
        
        self.base_currency=""
        self.base_amount=""

        self.targ_currencies=[]
        self.index=0

        self.latest={}
        self.mod_rates={}
        
    
    def resize(self,directory,width,height):
        base=Image.open(directory)
        resize=base.resize((width,height))
        photoimg=ImageTk.PhotoImage(resize)
        return photoimg  
    
    def widget_preset(self,bg='white',fg='white',font=('Tahoma',16)):
        preset = {'bg':bg,'fg':fg,'font':font}
        return preset
    
    def base_rm_curr(self,event):
        self.base_curr_entry.configure(fg=App.black)
        self.base_curr_entry.delete(0,tk.END)
        self.base_curr_entry.unbind("<FocusIn>")
    
    def base_on_curr_input(self,*args):
        # Get the input and turn into uppercase
        self.base_currency=self.base_curr_input.get().upper()

        # If the obtained string is a key-pair,
        if self.base_currency in self.valid_entries:
            # set the flag of the valid,
            self.base_upd_guis()
        else:
            # if not valid, change it to UNK (unknown)
            self.base_upd_guis(0)

            # and if "latest" has been pressed and an amount is input, update the table with 0 values, and update the converted amounts
            if self.latest and self.base_amount_input:
                self.update_table(0)
                self.targ_change_curr_amount()

        self.base_on_amount_input()

    def base_rm_amount(self,event):
        self.base_amount_entry.configure(fg=App.black)
        self.base_amount_entry.delete(0,tk.END)
        self.base_amount_entry.unbind("<FocusIn>")
        
    def get_latest(self):
        # Call the latest values
        self.latest=App.client.latest()
        #print(self.latest["data"])
        if self.base_amount:
            self.base_on_amount_input()

        messagebox.showinfo("Success!","Obtained latest currency data!")
        messagebox.showinfo("Info", f"Available Currencies: {[key for key in self.flags.keys()]}")

    def targ_rm_curr(self,event):
        self.targ_curr_entry.configure(fg=App.black)
        self.targ_curr_entry.delete(0,tk.END)
        self.targ_curr_entry.unbind("<FocusIn>")

    def targ_on_curr_input(self,*args):
        # Get the string, turn into all uppercase, then split into a list,
        # but only include those who are valid.
        self.targ_currencies=[i for i in self.targ_curr_input.get().upper().split(",") if i in self.valid_entries]
        
        # In the case of the length fluctuating inbetween writing,
            # if there is a valid currency, regardless of length,
        if self.targ_currencies:
                # check if the index is greater or equal than last positional index,
            if self.index>=len(self.targ_currencies)-1:
                    # reduce the index to the last positional.
                if self.index>0:
                    self.index=len(self.targ_currencies)-1
                    
        # Remove the buttons if the input has 1 in length or 0
        if len(self.buttons)==0 or 1:
                if len(self.buttons)>0:
                    self.destroy_buttons()

        # If we have 2+ valid currencies,
        if len(self.targ_currencies)>1:
            # In the case of our index not being the last positional,
            if self.index!=len(self.targ_currencies)-1:
                # create a "next" button, but only if it hasn't been created before
                if self.targ_next_frame not in self.buttons:
                    self.create_next_button()

            # In the case of our index not being the first positional,
            if self.index!=0:
                # create a "back" button, but only if there isn't one already
                if self.targ_back_frame not in self.buttons:
                    self.create_back_button()
        
        # Update the flags. Only after the index operations are done.
            # Default flag if no valid currency is entered.
        if not self.targ_currencies:
            self.targ_flag.configure(image=self.flags["UNK"])
            self.targ_curr_symbol.configure(text=self.symbols["UNK"])
            return
        
        # Flag if a value is entered, using index (default 0)
        self.targ_upd_guis()

    def base_on_amount_input(self,*args):
        # Obtain string
        self.base_amount=self.base_amount_input.get()

        # Check to see if the input string is only numbers
        if self.base_amount.isnumeric():
            # Turn the string into a number
            self.base_amount=int(self.base_amount)
            # If the base currency is valid and "latest" button has been pressed,
            if self.base_currency in self.valid_entries and self.latest:
                # Update table in success mode (using input amount)
                self.update_table()
        else:
            # If it's not all numbers, all values will be 0
            self.update_table(0)
        
        # Regardless how the table is updated, update the currencies
        self.targ_change_curr_amount()
     
    def base_upd_guis(self,success=1):
        if success:
            self.base_flag.configure(image=self.flags[self.base_currency])
            self.base_curr_symbol.configure(text=self.symbols[self.base_currency])
            return
        
        self.base_flag.configure(image=self.flags["UNK"])
        self.base_curr_symbol.configure(text=self.symbols["UNK"])   

    def update_table(self,success=1):
        if self.latest:
            if success:
                self.mod_rates=mod_rates(self.latest,self.base_currency,self.base_amount)
            else:
                
                self.mod_rates=mod_rates(self.latest,"USD",0)

    def targ_change_curr_amount(self):
        if self.targ_currencies and self.mod_rates:
            self.targ_amount_value.set(self.mod_rates[self.targ_currencies[self.index]])
            
    def destroy_buttons(self):
        for i in self.buttons:
            i.destroy()
        self.buttons.clear()

    def targ_upd_guis(self):
        # Change flag and symbol.
        self.targ_flag.configure(image=self.flags[self.targ_currencies[self.index]])
        self.targ_curr_symbol.configure(text=self.symbols[self.targ_currencies[self.index]])

        # If possible, change converted amount as well.
        if self.latest:
            self.targ_change_curr_amount()



























if __name__ =='__main__':
    App().mainloop()