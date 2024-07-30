import sys
sys.path.append(r'C:\Users\miraj\OneDrive\Desktop\Map_Extractor')
from imports import *
from threading import Thread
from scraping import main
from mail import email_process
from scrape_review import run_review_scrape


def handle_inputs():
    place_name = place_input.get()
    if not place_name:
        messagebox.showerror('Input Error', 'Place Name is required.')
        return
    
    # Write place_name to a file
    with open('place_and_keyword.txt', 'w') as file:
        file.write(f"{place_name}")

    messagebox.showinfo('Success', f'Scraping reviews for shop: {place_name}')
    
    # Run the scraping and email processing in a separate thread
    scraping_thread = Thread(target=scrape_and_process)
    scraping_thread.start()

def scrape_and_process():
    place_name = place_input.get()
    run_review_scrape(place_name)
    messagebox.showinfo('Success', f'Reviews Scraping is Finished. Check the output_reviews folder.')
    

def open_main_window():
    root.destroy()  # Close the current window
    import main_gui as mainwindow
    mainwindow.run_main_window()

def run_review_window():
    global root, place_input
    root = Tk()
    root.title('Review Scraping Tool')
    root.geometry('800x600')
    root.configure(background='#ecf0f1')

    # Load and resize the image
    img = Image.open('subwindows/th.jpg')
    resized_img = img.resize((120, 120))
    img = ImageTk.PhotoImage(resized_img)

    # Create a Label widget and set the image
    label = Label(root, image=img)
    label.pack(pady=(20,10))

    # Keep a reference to the image object to avoid garbage collection
    label.image = img

    text_label = Label(root, text='....REVIEWS SCRAPPING....', fg='white', bg='#0096DC')
    text_label.pack(fill='x', pady=(20,15))
    text_label.config(font=('verdana',15))

    place_label = Label(root, text='Enter Shop Name, Location Name: ', fg='white', bg='#e74c3c')
    place_label.pack(pady=(20,20))
    place_label.config(font=('verdana',14))

    place_input = Entry(root, width=60)
    place_input.pack(ipady=10, pady=(5,15))

    submit_btn = Button(root, text='Scrape', bg='#2c3e50', fg='white', width=20, height=2, command=handle_inputs)
    submit_btn.pack(pady=(30,50))
    submit_btn.config(font=('verdana',10))

    home_btn = Button(root, text='Home', bg='#219C90', fg='white', width=10, height=2, command=open_main_window)
    home_btn.config(font=('verdana', 10))
    home_btn.pack(side='left', padx=(30, 70))

    root.mainloop()

if __name__ == "__main__":
    run_review_window()
