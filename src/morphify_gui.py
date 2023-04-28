import os
import shutil
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from morphify import morphify

TEMP_DIR = os.environ.get('TEMP_DIR', './temp/')
STRANGER_MALE_DIR = os.environ.get('STRANGER_MALE_DIR', './stranger_male/')
STRANGER_FEMALE_DIR = os.environ.get('STRANGER_MALE_DIR', './stranger_female/')

assert os.path.exists(STRANGER_MALE_DIR), \
    f'STRANGER_MALE_DIR {STRANGER_MALE_DIR} not exists!'
assert os.path.exists(STRANGER_FEMALE_DIR), \
    f'STRANGER_FEMALE_DIR {STRANGER_FEMALE_DIR} not exists!'


def pack_files_and_morphify(i_photos: str,
                            friend_photos: str,
                            stranger_dir: str,
                            output_dir: str):
    try:
        assert i_photos, 'i_photos not selected!'
        assert friend_photos, 'friend_photos not selected!'
        assert stranger_dir, 'stranger_dir not selected!'
        assert output_dir, 'output_dir not selected!'
    except Exception as e:
        mb.showerror(message=e)
        return
    try:
        i_photos = eval(i_photos)
    except:
        mb.showerror(message=f'Bad i_photos selection: {i_photos}. '
                             f'Please select again.')
        return

    try:
        friend_photos = eval(friend_photos)
    except:
        mb.showerror(message=f'Bad friend_photos selection: {friend_photos}. '
                             f'Please select again.')
        return

    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
        for input_file in i_photos + friend_photos:
            shutil.copy(input_file,
                        os.path.join(TEMP_DIR, os.path.split(input_file)[1]))
        morphify(input_dir=TEMP_DIR,
                 stranger_dir=stranger_dir,
                 output_dir=output_dir)
        mb.showwarning(message=f'Morphing done!')
    except Exception as e:
        mb.showerror(message=e)


if __name__ == '__main__':
    tk.Tk()

    i_dir = tk.StringVar()
    friend_dir = tk.StringVar()
    stranger_dir_male_selected = tk.BooleanVar()  # Can't work with paths.
    output_dir = tk.StringVar()

    tk.Button(text='Select I photos',
              command=lambda: i_dir.set(fd.askopenfilenames())) \
        .pack(fill=tk.X)
    tk.Button(text='Select Friend photos',
              command=lambda: friend_dir.set(fd.askopenfilenames())) \
        .pack(fill=tk.X)

    stranger_dir_male_selected.set(True)
    tk.Radiobutton(text='Male Stranger',
                   variable=stranger_dir_male_selected, value=True).pack(
        fill=tk.X)
    tk.Radiobutton(text='Female Stranger',
                   variable=stranger_dir_male_selected, value=False).pack(
        fill=tk.X)

    tk.Button(text='Select output directory',
              command=lambda: output_dir.set(fd.askdirectory(mustexist=True))) \
        .pack(fill=tk.X)

    tk.Label().pack(fill=tk.X)

    tk.Button(text='Generate morphing frames',
              command=lambda: pack_files_and_morphify(
                  i_photos=i_dir.get(),
                  friend_photos=friend_dir.get(),
                  stranger_dir=STRANGER_MALE_DIR
                  if stranger_dir_male_selected.get() else STRANGER_FEMALE_DIR,
                  output_dir=output_dir.get()
              )).pack(fill=tk.X)
    tk.mainloop()
