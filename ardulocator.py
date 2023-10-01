import folium
import webbrowser
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from PIL import Image, ImageTk


def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            lat, lon, date, time = line.strip().split(',')
            coordinates.append((lat, lon, date, time))
    return coordinates


def plot_coordinates_on_map(coordinates):
    m = folium.Map(location=[float(coordinates[0][0]), float(coordinates[0][1])], zoom_start=10, tiles='OpenStreetMap')

    for i in range(len(coordinates) - 1):
        lat, lon, date, time = coordinates[i]
        next_lat, next_lon, next_date, next_time = coordinates[i + 1]

        popup_content = f"Date: {date}<br>Time: {time}"

        folium.Marker(location=[float(lat), float(lon)], popup=popup_content).add_to(m)
        folium.PolyLine(locations=[(float(lat), float(lon)), (float(next_lat), float(next_lon))], color='blue').add_to(
            m)
        folium.RegularPolygonMarker(location=[float(next_lat), float(next_lon)], fill_color='green', number_of_sides=3,
                                    radius=10, popup=popup_content).add_to(m)

    return m


def create_map_and_open_html(file_path):
    coordinates = read_coordinates(file_path)
    map_with_markers = plot_coordinates_on_map(coordinates)
    html_file = "map.html"
    map_with_markers.save(html_file)
    webbrowser.open(html_file)


def drop(event):
    file_path = event.data
    create_map_and_open_html(file_path)


def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        create_map_and_open_html(file_path)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Ardulocator")
    root.geometry("231x286")
    root.configure(bg="thistle4")
    root.iconbitmap("logo.ico")
    root.resizable(False, False)

    img = Image.open("dragandrop.png")
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=photo, bg="thistle4")
    label.image = photo
    label.pack(pady=30)

    button = tk.Button(root, text="Select Files", command=select_file, bg="#00979c", fg="white",
                       font=("Helvetica", 12, "bold"), padx=20, pady=10, borderwidth=0, activebackground="#2980b9")
    button.pack()

    sign = tk.Label(root, text="By eymencakmak", anchor="se", bg="thistle4")
    sign.pack(side="right", padx=10, pady=10)

    version = tk.Label(root, text="Version:1.0.0", anchor="sw", bg="thistle4")
    version.pack(side="left", padx=10, pady=10)

    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    root.mainloop()
