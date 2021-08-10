from _thread import start_new_thread
from tkinter import *

from win10toast import ToastNotifier

from loader_script import SeleniumImageLoader

import os
import json
import re

window = Tk()
text = Text(window, width=25, height=50)
text.pack(side=LEFT)
frame = Frame()
frame.pack()
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)

comment = Label(window, text="<-- Enter your text here", fg='red', font=("Helvetica", 16))
comment.place(x=230, y=15)
comment2 = Label(window, text="Separate each element by ';' ", fg='red', font=("Helvetica", 12))
comment2.place(x=460, y=18)

driver_path_string_var = StringVar()
target_folder = StringVar()
quantity = StringVar()
ready_folder = StringVar()


def save_config():
    config = {}
    config['driver path'] = driver_path_string_var.get()
    config['target folder'] = target_folder.get()
    config['quantity'] = int(quantity.get())
    config['ready folder'] = ready_folder.get()
    with open('config_file.json', 'w', encoding='utf8') as cfg:
        json.dump(config, cfg, indent=4, ensure_ascii=False)
    print(config)
    cfg.close()


save_config_button = Button(window, text="Save Config", command=save_config)
save_config_button.place(x=350, y=420)


def load_config():
    with open('config_file.json', encoding='utf8') as cfg:
        json.data = json.load(cfg, encoding='utf8')

    driver_path_string_var.set(json.data['driver path'])
    target_folder.set(json.data['target folder'])
    quantity.set(json.data['quantity'])
    ready_folder.set(json.data['ready folder'])
    print(driver_path_string_var.get())
    print(target_folder.get())
    print(quantity.get())
    print(ready_folder.get())


load_config_button = Button(window, text="Load Config", command=load_config)
load_config_button.place(x=350, y=450)

driver_path_entry = Entry(window, font=("Helvetica", 12), bd=5, textvariable=driver_path_string_var)
driver_path_entry.place(x=440, y=50)
folderDirection = Entry(window, font=("Helvetica", 12), bd=5, textvariable=target_folder)
folderDirection.place(x=440, y=120)
number = Entry(window, font=("Helvetica", 12), bd=5, textvariable=quantity)
number.place(x=440, y=190)
ready_folder_entry = Entry(window, font=("Helvetica", 12), bd=5, textvariable=ready_folder)
ready_folder_entry.place(x=440, y=260)

pathLabel = Label(window, text="Driver path: ", font=("Helvetica", 16))
pathLabel.place(x=230, y=50)
numberLabel = Label(window, text="Images per request: ", font=("Helvetica", 16))
numberLabel.place(x=230, y=190)
folderLabel = Label(window, text="Save to folder: ", font=("Helvetica", 16))
folderLabel.place(x=230, y=120)
ready_folder_label = Label(window, text="Ready Folder", font=("Helvetica", 16))
ready_folder_label.place(x=230, y=260)


def click():
    splited = text.get("1.0", "end-1c").split(';')
    try:
        image_loader = SeleniumImageLoader(driver_path_string_var.get(), target_folder.get())
        image_loader.load_images(splited, int(quantity.get()))

    except Exception as e:
        print(e)
        toaster = ToastNotifier()
        toaster.show_toast("Attention", str(e), icon_path=None, duration=100)



btn = Button(window, text="Download", fg='blue', command=click)
btn.place(x=580, y=450)


def numbers_deleting():
    if not os.path.exists(ready_folder.get()):
        os.mkdir(ready_folder.get())

    file_names = os.listdir(ready_folder.get())
    print(file_names)
    saved_path = os.getcwd()
    os.chdir(saved_path)
    print("Current working directory is " + saved_path)
    os.chdir(ready_folder.get())

    for file_name in file_names:
        try:
            x = re.match("(.*)?[0-9]+\.jpg", file_name)
            print(x.group(1))
            new_file_name = x.group(1)
            #            #x=re.match("(.*)[0-9]+\.jpg", file_name) # <-- Wrong regex region
            #            print("New filename is " + file_name.strip('0123456789.jpg') + '.jpg')
            os.replace(file_name, new_file_name + '.jpg')
        except Exception as e:
            print(e)
            toaster = ToastNotifier()
            toaster.show_toast("Attention", str(e), icon_path=None, duration=100)

    os.chdir('..')


delete_numbers_button = Button(window, text="Delete numbers", command=numbers_deleting)
delete_numbers_button.place(x=460, y=420)


def target_folder_file_renaming():
    downloaded_image_names = os.listdir(target_folder.get())
    print(downloaded_image_names)
    saved_path = os.getcwd()
    os.chdir(saved_path)
    print("Current working directory is " + saved_path)
    os.chdir(target_folder.get())

    new_image_list = []

    for name in downloaded_image_names:
        try:
            x = re.match("([^\d]+)[0-9]+\.jpg", name)
            print(x.group(1))
            new_file_name = x.group(1)
            os.replace(name, new_file_name + '.jpg')
        except Exception as e:
            print(e)
            toaster = ToastNotifier()
            toaster.show_toast("Attention", str(e), icon_path=None, duration=100)

        new_image_list.append(name)
    set(new_image_list)

    os.chdir('..')


def checking_existing_files():
    images_names = text.get("1.0", "end-1c").split(';')
    for i in range(len(images_names)):
        images_names[i] = images_names[i].strip()
    chosen_images = os.listdir(ready_folder.get())
    chosen_images_names = []
    for chosen_image in chosen_images:
        x = re.match("(.*?)\.jpg", chosen_image)
        chosen_images_names.append(x.group(1))
    images_names = list(set(images_names) - set(chosen_images_names))
    text.delete(1.0, "end")
    text.insert(1.0, ';'.join(images_names))


display_missing_images_button = Button(window, text='Change filenames', command=checking_existing_files, fg='red')
display_missing_images_button.place(x=460, y=450)

window.title('Image Downloader')
window.geometry("680x500+350+150")
window.resizable(width=False, height=False)
window.mainloop()
