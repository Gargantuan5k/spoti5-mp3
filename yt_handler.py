from pytube import YouTube, Search
from pprint import pprint
import os


def percent(self, tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc


def progress_function(self,stream, chunk,file_handle, bytes_remaining):

    size = stream.filesize
    p = 0
    while p <= 100:
        progress = p
        print(str(p)+'%')
        p = percent(bytes_remaining, size)


def search(song, artist, album=None, destination='.'):
    yt_details_list = []
    yt_list = []

    if album:
        res = Search(f"{artist} {song} album {album}")
    else:
        res = Search(f"{artist} {song}")
    ids = [i.video_id for i in res.results]
    for i in ids:
        link = f"https://www.youtube.com/watch?v={i}"
        yt = YouTube(link, on_progress_callback=progress_function)
        yt_details_dict = {
            'title': yt.title,
            'channel': yt.author,
            'id': yt.video_id,
            'url': yt.watch_url
        }
        yt_details_list.append(yt_details_dict)
        yt_list.append(yt)


    return yt_list, yt_details_list
        

def get(tracks_to_get):
    q_ytl = dict()
    q_ytdl = dict()
    for idx, i in enumerate(tracks_to_get):
        ytl, ytdl = search(song=i[0], artist=i[1]) # ytl and ytdl are for each track in tracks_to_get
        q_ytl[idx] = ytl
        q_ytdl[idx] = ytdl
    
    # pprint(q_ytdl)
    return q_ytl, q_ytdl


def download(yt_objs, destination=os.getcwd()):
    for yt in yt_objs:
        filtered = yt.streams.filter(only_audio=True)
        try:
            stream = filtered[0]
            # TODO put multiple files into a folder (maybe zip it)
            stream.download(output_path=destination)
        except IndexError:
            print('IndexError! No available streams to download.')


if __name__ == "__main__":
    pprint(search('Look What You Made Me Do', 'Taylor Swift', album="Reputation")[1])
    print('\n\n\n\n')
    pprint(search('Never Gonna Give You Up', 'Rick Astley')[1])
    print('\n\n\n')
    pprint(search('Bones', 'Imagine Dragons')[1])

    # get([('Never Gonna Give You Up', 'Rick Astley'), ('Bones', 'Imagine Dragons'), ('As It Was', 'Harry Styles')])