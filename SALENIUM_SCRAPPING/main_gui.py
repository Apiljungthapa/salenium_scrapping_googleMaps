import sys
import os
from imports import *
from threading import Thread
from scraping import main
from mail import email_process

def handle_inputs():
    place_name = place_input.get()
    keyword = keyword_input.get()

    if not place_name:
        messagebox.showerror('Input Error', 'Place Name is required.')
        return
    if not keyword:
        messagebox.showerror('Input Error', 'Keyword is required.')
        return
    
    # Write place_name and keyword to a file
    with open('place_and_keyword.txt', 'w') as file:
        file.write(f"{place_name}\n{keyword}")

    messagebox.showinfo('Success', f'Scraping data for place: {place_name} with keyword: {keyword}')
    
    # Run the scraping and email processing in a separate thread
    scraping_thread = Thread(target=scrape_and_process) 
    scraping_thread.start()

def scrape_and_process():
    dframe = main()
    messagebox.showinfo('Success', f'Scraping is Finished. Check the output folder. It takes 15-20 minutes for emails.')
    
    email_process(dframe)
    messagebox.showinfo('Success', f'Scraping with Emails is Finished. Check the output_with_emails folder.')

def open_review_window():
    root.destroy()  # Close the current window
    import subwindows.review_gui as reviewgui
    reviewgui.run_review_window()

def run_main_window():
    global root, place_input, keyword_input
    root = Tk()
    root.title('Map Scraping Tool')
    root.geometry('800x600')
    root.configure(background='#ecf0f1')

    # Load and resize the image
    img = Image.open('wallpapers/img1.jpg')
    resized_img = img.resize((120, 120))
    img = ImageTk.PhotoImage(resized_img)

    # Create a Label widget and set the image
    label = Label(root, image=img)
    label.pack(pady=(20,10))

    # Keep a reference to the image object to avoid garbage collection
    label.image = img

    text_label = Label(root, text='....MAP SCRAPPING....', fg='white', bg='#0096DC')
    text_label.pack(fill='x', pady=(20,15))
    text_label.config(font=('verdana',15))

    place_label = Label(root, text='Enter Place Name: ', fg='white', bg='#e74c3c')
    place_label.pack(pady=(20,10))
    place_label.config(font=('verdana',14))

    place_input = Entry(root, width=50)
    place_input.pack(ipady=10, pady=(5,15))

    keyword_label = Label(root, text='Enter Keyword: ', fg='white', bg='#e74c3c')
    keyword_label.pack(pady=(20,10))
    keyword_label.config(font=('verdana',14))

    keyword_input = Entry(root, width=70)
    keyword_input.pack(ipady=10, pady=(5,15))

    submit_btn = Button(root, text='Scrape', bg='#2c3e50', fg='white', width=20, height=2, command=handle_inputs)
    submit_btn.pack(pady=(30,20))
    submit_btn.config(font=('verdana',10))

    review_btn = Button(root, text='Scrape Reviews', bg='#219C90', fg='white', width=20, height=2, command=open_review_window)
    review_btn.config(font=('verdana', 10))
    review_btn.pack(side='left', padx=(5, 70))

    root.mainloop()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    run_main_window()
