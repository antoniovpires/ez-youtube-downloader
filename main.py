import tkinter
import customtkinter
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable

def append_stream(quality, itag):
    streams.append({
            "quality": quality,
            "itag": itag 
        })

def radiobutton_event():
    global stream_type
    stream_type = radio_var.get()

def handle_input(*args):
    global streams

    streams = list()
    input_text = link.get()
    yt_object = YouTube(input_text)
    avaiable_res = set()
    avaiable_audios = set()

    for stream in yt_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc():
        avaiable_res.add(stream.resolution)
        append_stream(stream.resolution, stream.itag)
    
    for stream in yt_object.streams.filter(only_audio=True):
        avaiable_audios.add(stream.abr)
        append_stream(stream.abr, stream.itag)


    global resolutionOptions 
    radiobutton_1 = customtkinter.CTkRadioButton(app, text="Video and Audio",
                                                command=radiobutton_event, variable= radio_var, value=1)
    radiobutton_1.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
    resolutionOptions = customtkinter.CTkOptionMenu(app, values=list(avaiable_res))
    resolutionOptions.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

    global audioOptions 
    radiobutton_2 = customtkinter.CTkRadioButton(app, text="Audio Only",
                                                command=radiobutton_event, variable= radio_var, value=2)
    radiobutton_2.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
    audioOptions = customtkinter.CTkOptionMenu(app, values=list(avaiable_audios))
    audioOptions.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

    download.grid(row=7, column=0, padx=20, pady=20, sticky="ew", columnspan=2)


def startDownload():
    try:
        pPercentage.grid(row=5, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        progressBar.grid(row=6, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)

        if stream_type == 1:
            chosen_res = resolutionOptions.get()
        else:
            chosen_res = audioOptions.get()
 
        for option in streams:
            if option["quality"] == chosen_res:
                video = ytObject.streams.get_by_itag(option["itag"])            

        title.configure(text=ytObject.title)
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Downloaded successfully!", text_color="green")
        pPercentage.grid_remove()
        progressBar.grid_remove()
    except RegexMatchError:
        finishLabel.configure(text="The provided YouTube link is invalid.", text_color="red")
    except VideoUnavailable:
        finishLabel.configure(text="The requested video is not available.", text_color="red")
    except Exception as e:
        finishLabel.configure(text=f"An error occurred: {str(e)}", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    # Update progress bar
    progressBar.set(float(percentage_of_completion) / 100)
    
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()


# System Settings

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Our app frame
app = customtkinter.CTk()
app.title("EZ-YT Downloader")
app.geometry("720x480")
app.grid_columnconfigure((0, 1), weight=1)

## Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a youtube link and press Enter")
title.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.bind('<Return>', handle_input)
link.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

#  Progress percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)


# Streams Object
radio_var = tkinter.IntVar(value=0)


# Run app
app.mainloop()