from __future__ import print_function, unicode_literals
from prompt_toolkit.validation import Validator, ValidationError
from spotify_handler import get_tracks_from_playlist
import yt_handler
from pprint import pprint
import os
import questionary
from tkinter import Tk
from tkinter import filedialog


class LinkValidator(Validator):
    def validate(self, case, lnk):
        pass # TODO validation of playlist link


def get_from_file(fname):
    with open(f'ascii/{fname}', 'r') as f:
        return f.read()


def main_menu_prompt():
    ans = questionary.select(
        "Choose a menu option:",
        choices= [
            'I have a Spotify Playlist Link',
            # 'I have a Spotify Song Link'
            # 'I want to use the GUI version',
            'I need help using this!',
            'Exit'
        ]
    ).ask()
    
    return ans


def link_prompt(case="pl"):
    if case == 'pl':
        pl_lnk = questionary.text('Enter your Playlist Link:').ask() # TODO Add validation
        return pl_lnk
    
    elif case == 'sl':
        pass # TODO direct song link support


def tracks_to_get_prompt(track_list):
    ans2 = questionary.checkbox(
        "Select Songs to Download",
        choices=[
            f"({idx+1}) {track[0]} (ARTIST: {track[1]}, ALBUM: {track[2]})" for idx, track in enumerate(track_list)
            ]
    ).ask()

    res = []
    for i in ans2:
        idx_str = ''
        for j in i:
            if j.isnumeric():
                idx_str += j
            if j == ')': break
        idx = int(idx_str) - 1
        res.append(track_list[idx])

    return res


def get_yt(tracks_to_get):
    q_ytl, q_ytdl = yt_handler.get(tracks_to_get) # results for all the given queries
    d_ytl = []
    for k, v in q_ytdl.items(): # for each track (<number k>, <list of search results v>)
        possible_titles = []
        for idx, vobj in enumerate(v):
            possible_titles.append(f'({idx+1}) {vobj["title"]} - {vobj["channel"]}')

        os.system('cls')
        ans = questionary.select(
            f'Choose the closest matching track name for track number {k+1} [{tracks_to_get[k][1]} - {tracks_to_get[k][0]}]:',
            choices=possible_titles
        ).ask()

        idx_str = ''
        for i in ans:
            if i.isnumeric():
                idx_str += i
            if i == ')': break
        idx = int(idx_str) - 1

        d_ytl.append(q_ytl[k][idx]) # list of YouTube() objects

    return d_ytl


def get_destination():
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()

    dest = filedialog.askdirectory()
    return dest


def main_menu():
    while True:
        try:
            os.system('cls')
            print(get_from_file('spoti5-mp3.txt'))
            menu_pr_ans = main_menu_prompt()

            match menu_pr_ans:
                case 'I have a Spotify Playlist Link':
                    lpr_ans = link_prompt(case='pl') # link to pl

                    track_list = get_tracks_from_playlist(lpr_ans) # tuple(<track_name>, <artist_name>, <album>)
                    tracks_to_get = tracks_to_get_prompt(track_list)
                
                    ytdl_list = get_yt(tracks_to_get)
                    destination = get_destination() 

                    yt_handler.download(yt_objs=ytdl_list, destination=destination)
                    continue

                case 'I have a Spotify Song Link':
                    pass # TODO direct song link support

                case 'I need help using this!':
                    os.system('cls')
                    print(get_from_file('help.txt'))
                    input()
                    os.system('cls')
                    continue
                
                case 'Exit':
                    os.system('cls')
                    print(get_from_file('thanks.txt'))
                    break

                case _:
                    pass
        except:
            continue
    

if __name__ == "__main__":
    main_menu()
