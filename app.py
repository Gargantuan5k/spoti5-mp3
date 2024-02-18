from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from examples import custom_style_2
from prompt_toolkit.validation import Validator, ValidationError
from spotify_handler import get_tracks_from_playlist
import yt_handler
from pprint import pprint
import os


class LinkValidator(Validator):
    def validate(self, case, lnk):
        pass # TODO validation of playlist link


def get_from_file(fname):
    with open(f'ascii/{fname}', 'r') as f:
        return f.read()


def main_menu_prompt():
    question = {
        'type': 'list',
        'name': 'main_menu',
        'message': 'Choose a Menu Option',
        'choices': [
            'I have a Spotify Playlist Link',
            {
                'name': 'I have a Spotify Song Link',
                'disabled': 'Coming Soon!'
            },
            {
                'name': 'Use GUI/WebApp Mode',
                'disabled': 'Coming Soon!'
            },
            'I need help using this!'
        ]
    }
    os.system('cls')
    ans = prompt(question, style=custom_style_2)
    return ans


def link_prompt(case="pl"):
    if case == 'pl':
        question = {
            'type': 'input',
            'name': 'pl_lnk',
            'message': 'Enter the Playlist Link',
            'default': 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=77d8f5cd51cd478d'
        }
        lpr_ans = prompt(question, style=custom_style_2)
        return lpr_ans['pl_lnk']
    
    elif case == 'sl':
        pass # TODO direct song link support


def tracks_to_get_prompt(track_list):
    question1 = {
        'name': 'select_all',
        'type': 'confirm',
        'message': 'Select all tracks from this playlist?',
        'default': True
    }
    os.system('cls')
    ans1 = prompt(question1, style=custom_style_2)['select_all']
    if ans1:
        return track_list
    else:
        question2 = {
            'type': 'checkbox',
            'qmark': '🎵',
            'message': 'Select Songs to Download',
            'name': 'track_list',
            'choices': [{'name': f"({idx+1}) {track[0]} (ARTIST: {track[1]}, ALBUM: {track[2]})"} for idx, track in enumerate(track_list)],
            'validate': lambda answer: 'Choose at least one song!' if len(answer) == 0 else True
        }

        os.system('cls')
        ans2 = prompt(question2, style=custom_style_2)['track_list']
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
            possible_titles.append(f'({idx+1}) {vobj["title"]}')

        question = {
            'type': 'list',
            'name': 'track',
            'message': f'Choose the closest matching track name for track number {k+1} [{tracks_to_get[k][1]} - {tracks_to_get[k][0]}]',
            'choices': possible_titles
        }

        os.system('cls')
        ans = prompt(question, style=custom_style_2)['track']

        idx_str = ''
        for i in ans:
            if i.isnumeric():
                idx_str += i
            if i == ')': break
        idx = int(idx_str) - 1

        d_ytl.append(q_ytl[k][idx]) # list of YouTube() objects

    return d_ytl


def main_menu():
    print(get_from_file('spoti5-mp3.txt'))
    print(get_from_file('main_menu.txt'))
    menu_pr_ans = main_menu_prompt()['main_menu']

    match menu_pr_ans:
        case 'I have a Spotify Playlist Link':
            lpr_ans = link_prompt(case='pl') # link to pl

            track_list = get_tracks_from_playlist(lpr_ans) # tuple(<track_name>, <artist_name>, <album>)
            tracks_to_get = tracks_to_get_prompt(track_list)
        
            ytdl_list = get_yt(tracks_to_get)
            destination = get_destination() # TODO Implement getting output directory

            yt_handler.download(yt_objs=ytdl_list, destination=destination)
        case 'I have a Spotify Song Link':
            pass # TODO direct song link support

        case _:
            pass
    

if __name__ == "__main__":
    main_menu()
