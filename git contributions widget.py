from bs4 import BeautifulSoup
from urllib3 import PoolManager, exceptions as urexceptions
from time import sleep, strftime
from urllib.request import urlretrieve
from urllib.error import URLError
from tkinter import*
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from threading import Thread
from http.client import RemoteDisconnected

#SCRAPE THE CONTRIBUTIONS AND THE PROFILE BILD ON GITHUBE
def get_contributions(username: str) -> dict:
    url = f"https://github.com/{username}/"
    http = PoolManager()
    page = http.urlopen('GET', url)
    soup = BeautifulSoup(page.data, "html.parser")
    profil_bild = soup.find('img', attrs={'class': 'avatar avatar-user width-full border color-bg-default'})['src']
    
    tableau = soup.find(name='svg', attrs={'class': 'js-calendar-graph-svg'}) #TABLEAU OF CONTRIBUTIONS
    days = tableau.find_all(name='rect', attrs={'class': 'ContributionCalendar-day'}) #DAYS OF THE YEAR
    today = int(days[-1]['data-count'])

    last_month = int()
    for element in days[-int(strftime('%d'))]:
        last_year+=int(element['data-count'])

    last_year = int()
    for element in days:
        last_year+=int(element['data-count'])
    

    return {'year': last_year, 'month': last_month, 'day': today, 'profil_bild': profil_bild}

#DOWNLOAD A BILD
def download_bild(url: str, chemin: str) -> None:
    urlretrieve(url, chemin)
    img = PIL_Image.open(chemin)
    img = img.resize((40, 40))
    img.save(chemin)

def get_username(event=None) -> str:
    global username
    def validate(event):
        global username
        username = entry_user.get().strip() if entry_user.get().strip() != '' else username
        root_user.destroy()
        print(1)

    def f(event):
        root_user.destroy()
    
    root_user = Tk()
    label = Label(root_user, text='Enter the users name.\nControl-Entry to validate.')
    label.pack()

    entry_user = Entry(root_user)
    entry_user.insert(0, username)
    entry_user.pack()
    entry_user.focus_force()
    
    root_user.bind('<Control-Return>', validate)
    entry_user.bind('<Control-Return>', validate)
    root_user.bind('<Escape>', f)
    print(4)
    root_user.mainloop()
    
    get_contributions(username)
    w = open('data.txt', 'w', encoding='UTF-8')
    w.write(username)
    w.close()

    return username


#WENN THE USER MOVE THE WINDOW
def deplacement(event=None) -> None:
    try:
        x_souris, y_souris = root.winfo_pointerxy()
        x_root = root.winfo_width()
        y_root = root.winfo_height()

        x_souris-=round(x_root/2)
        y_souris-=round(y_root/2)
        
        
        if (root.winfo_screenwidth()-x_root+25) > x_souris > (root.winfo_screenwidth()-x_root-25):
            x_souris = root.winfo_screenwidth()-x_root
        elif -25 < x_souris < 25:
            x_souris = 0
        
        if (root.winfo_screenheight()-y_root+25) > y_souris > (root.winfo_screenheight()-y_root-25):
            y_souris = root.winfo_screenheight()-y_root
        elif -25 < y_souris < 25:
            y_souris = 0
        root.geometry(f"{x_root}x{y_root}+{x_souris}+{y_souris}")
        root.overrideredirect(True)
    except:
        pass

#MAKE THE WINDOWS MORE TRANSPARENT
def more_transparence(event=None) -> None:
    alpha = root.attributes('-alpha')
    if alpha<=0.95:
        root.attributes('-alpha', alpha+0.05)
    root.overrideredirect(True)

#MAKE THE WINDOWS LESS TRANSPARENT
def less_transparence(event=None) -> None:
    alpha = root.attributes('-alpha')
    if alpha>=0.10:
        root.attributes('-alpha', alpha-0.05)
    root.overrideredirect(True)

#CLOSE THE WINDOWS
def fermer(event=None) -> None:
    root.destroy()


#UPDATE THE ROOT WITH NEW INFOS
def update_root(event=None) -> None:
    n = get_contributions(username)
    if len(str(n['day']))<2:
        n['day']=' '+str(n['day'])
    var_day.set(n['day'])

    if n['day'] == 0:
        label_day_contr['bg'] = '#161b22'
    elif n['day'] == 1:
        label_day_contr['bg'] = '#0e4429'
    elif n['day'] == 2:
        label_day_contr['bg'] = '#006d32'
    elif n['day'] == 3:
        label_day_contr['bg'] = '#26a641'
    else:
        label_day_contr['bg'] = '#39d353'
    
    download_bild(n['profil_bild'], 'profil_bild.png')

#CALL "UPDATE_ROOT" IN A LOOP WITH SLEEP 
def main() -> None:
    deplacement()
    while True:
        try:
            update_root()
            im = PIL_ImageTk.PhotoImage(PIL_Image.open('profil_bild.png').resize((40, 40)))
            canvas.create_image(20, 20, image=im)
            sleep(5)
        except RuntimeError:#WINDOWS CLOSED
            break
        except AttributeError:#WINDOWS CLOSED
            break
        except urexceptions.MaxRetryError:#NETWERK
            sleep(5)
        except URLError:#NETWERK
            sleep(5)
        except RemoteDisconnected:#NETWERK
            sleep(5)
        except TypeError:
            username = get_username()
        
        

#USR WICH BE SCRAPPED
username = str()
try:
    username = open('data.txt', 'r', encoding='UTF-8').read()
except FileNotFoundError:
    username = get_username()

root = Tk()
var_day = StringVar(value=' 0')

root.config(bg='#0d1117')
root.geometry("80x40")
root.attributes("-topmost", True)
root.overrideredirect(True)
root.attributes('-alpha', 0.7)

root.bind('<Escape>', fermer)
root.bind('<B1-Motion>', deplacement)
root.bind('<Control-Up>', more_transparence)
root.bind('<Control-Down>', less_transparence)
root.bind('<Control-r>', update_root)
root.bind('<Control-s>', get_username)

frame_all = Frame(root, bg='#0d1117')
frame_all.pack(expand=YES)

canvas = Canvas(root, width=40, height=40, bg='#0d1117', highlightbackground='#0d1117')
canvas.pack(side=LEFT)

can_label = Canvas(root, width=30, height=40, bg='#0d1117', highlightbackground='#0d1117')
can_label.pack(side=LEFT)

label_day_contr = Label(can_label, textvariable=var_day, font=('', 19), bg='#161b22', fg='black')
can_label.create_window(15, 20, window=label_day_contr)

try:
    im = PIL_ImageTk.PhotoImage(PIL_Image.open("profil_bild.png").resize((40, 40)))
    canvas.create_image(20, 20, image=im)
except:
    canvas.create_image(20, 20)
Thread(target=main).start()
root.mainloop()