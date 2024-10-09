from tkinter import filedialog, Tk

def choose_file():
    root = Tk()
    root.withdraw()
    file = filedialog.askopenfilename(
    filetypes = [("csv files", "*.csv"),
                 ("Excel files", "*.xlsx;*.xls"),
                 ("SQlite databases", "*.sqlite;*.db")]
    )
choose_file()