import tkinter as tk
from tkinter import colorchooser
from skimage import color
import numpy as np

def convert_color(rgb):
    rgb_norm = np.array(rgb) / 255
    lab = color.rgb2lab([[rgb_norm]])[0][0]
    xyz = rgb_to_xyz(rgb_norm)
    return lab, xyz

def rgb_to_xyz(rgb):
    xyz = color.rgb2xyz([[rgb]])[0][0]
    return round(xyz[0], 2), round(xyz[1], 2), round(xyz[2], 2)

def xyz_to_rgb(xyz):
    rgb = color.xyz2rgb([[xyz]])
    rgb_clipped = np.clip(rgb, 0, 1)
    return [int(c * 255) for c in rgb_clipped[0][0]]

def lab_to_rgb(lab):
    rgb = color.lab2rgb(np.array([[lab]]))
    rgb_clipped = np.clip(rgb, 0, 1)
    return [int(c * 255) for c in rgb_clipped[0][0]]

def update_fields(rgb):
    lab, xyz = convert_color(rgb)

    lab_l_entry.delete(0, tk.END)
    lab_l_entry.insert(0, round(lab[0], 2))
    lab_a_entry.delete(0, tk.END)
    lab_a_entry.insert(0, round(lab[1], 2))
    lab_b_entry.delete(0, tk.END)
    lab_b_entry.insert(0, round(lab[2], 2))

    xyz_x_entry.delete(0, tk.END)
    xyz_x_entry.insert(0, round(xyz[0], 2))
    xyz_y_entry.delete(0, tk.END)
    xyz_y_entry.insert(0, round(xyz[1], 2))
    xyz_z_entry.delete(0, tk.END)
    xyz_z_entry.insert(0, round(xyz[2], 2))

    rgb_r_entry.delete(0, tk.END)
    rgb_r_entry.insert(0, rgb[0])
    rgb_g_entry.delete(0, tk.END)
    rgb_g_entry.insert(0, rgb[1])
    rgb_b_entry.delete(0, tk.END)
    rgb_b_entry.insert(0, rgb[2])

    rgb_r_scale.set(rgb[0])
    rgb_g_scale.set(rgb[1])
    rgb_b_scale.set(rgb[2])

    lab_l_scale.set(lab[0])
    lab_a_scale.set(lab[1])
    lab_b_scale.set(lab[2])

    xyz_x_scale.set(xyz[0])
    xyz_y_scale.set(xyz[1])
    xyz_z_scale.set(xyz[2])

    r, g, b = validate_rgb_value(rgb[0]), validate_rgb_value(rgb[1]), validate_rgb_value(rgb[2])
    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

def validate_rgb_value(value):
    return max(0, min(255, int(value)))

def choose_color():
    color_code = colorchooser.askcolor(title="Выберите цвет")
    if color_code and color_code[0]:
        rgb = tuple(map(int, color_code[0]))
        update_fields(rgb)

def on_lab_change(event=None):
    try:
        l = float(lab_l_entry.get())
        a = float(lab_a_entry.get())
        b = float(lab_b_entry.get())
        rgb = lab_to_rgb([l, a, b])
        update_fields(rgb)
    except ValueError:
        pass

def on_xyz_change(event=None):
    try:
        x = float(xyz_x_entry.get())
        y = float(xyz_y_entry.get())
        z = float(xyz_z_entry.get())
        rgb = xyz_to_rgb([x, y, z])
        update_fields(rgb)
    except ValueError:
        pass

def on_rgb_change(event=None):
    try:
        r = int(rgb_r_entry.get())
        g = int(rgb_g_entry.get())
        b = int(rgb_b_entry.get())
        update_fields([r, g, b])
    except ValueError:
        pass

root = tk.Tk()
root.title("Преобразование цветовых моделей")
root.geometry("800x600")

color_display = tk.Label(root, text="Цвет", bg="white", width=20, height=10)
color_display.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="ew")

color_button = tk.Button(root, text="Выбрать цвет", command=choose_color, font=("Helvetica", 14))
color_button.grid(row=1, column=0, columnspan=6, pady=10, padx=10)

tk.Label(root, text="LAB", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
lab_l_entry = tk.Entry(root, width=10)
lab_a_entry = tk.Entry(root, width=10)
lab_b_entry = tk.Entry(root, width=10)
lab_l_entry.grid(row=2, column=1, padx=5, pady=5)
lab_a_entry.grid(row=2, column=2, padx=5, pady=5)
lab_b_entry.grid(row=2, column=3, padx=5, pady=5)
lab_l_entry.bind("<KeyRelease>", on_lab_change)
lab_a_entry.bind("<KeyRelease>", on_lab_change)
lab_b_entry.bind("<KeyRelease>", on_lab_change)

lab_l_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda val: on_lab_change())
lab_a_scale = tk.Scale(root, from_=-128, to=127, orient=tk.HORIZONTAL, command=lambda val: on_lab_change())
lab_b_scale = tk.Scale(root, from_=-128, to=127, orient=tk.HORIZONTAL, command=lambda val: on_lab_change())
lab_l_scale.grid(row=2, column=4, padx=5, pady=5)
lab_a_scale.grid(row=2, column=5, padx=5, pady=5)
lab_b_scale.grid(row=2, column=6, padx=5, pady=5)

tk.Label(root, text="XYZ", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5)
xyz_x_entry = tk.Entry(root, width=10)
xyz_y_entry = tk.Entry(root, width=10)
xyz_z_entry = tk.Entry(root, width=10)
xyz_x_entry.grid(row=3, column=1, padx=5, pady=5)
xyz_y_entry.grid(row=3, column=2, padx=5, pady=5)
xyz_z_entry.grid(row=3, column=3, padx=5, pady=5)
xyz_x_entry.bind("<KeyRelease>", on_xyz_change)
xyz_y_entry.bind("<KeyRelease>", on_xyz_change)
xyz_z_entry.bind("<KeyRelease>", on_xyz_change)

xyz_x_scale = tk.Scale(root, from_=0, to=95, resolution=0.1, orient=tk.HORIZONTAL, command=lambda val: on_xyz_change())
xyz_y_scale = tk.Scale(root, from_=0, to=100, resolution=0.1, orient=tk.HORIZONTAL, command=lambda val: on_xyz_change())
xyz_z_scale = tk.Scale(root, from_=0, to=108, resolution=0.1, orient=tk.HORIZONTAL, command=lambda val: on_xyz_change())
xyz_x_scale.grid(row=3, column=4, padx=5, pady=5)
xyz_y_scale.grid(row=3, column=5, padx=5, pady=5)
xyz_z_scale.grid(row=3, column=6, padx=5, pady=5)

tk.Label(root, text="RGB", font=("Helvetica", 12)).grid(row=4, column=0, padx=10, pady=5)
rgb_r_entry = tk.Entry(root, width=10)
rgb_g_entry = tk.Entry(root, width=10)
rgb_b_entry = tk.Entry(root, width=10)
rgb_r_entry.grid(row=4, column=1, padx=5, pady=5)
rgb_g_entry.grid(row=4, column=2, padx=5, pady=5)
rgb_b_entry.grid(row=4, column=3, padx=5, pady=5)
rgb_r_entry.bind("<KeyRelease>", on_rgb_change)
rgb_g_entry.bind("<KeyRelease>", on_rgb_change)
rgb_b_entry.bind("<KeyRelease>", on_rgb_change)

rgb_r_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda val: on_rgb_change())
rgb_g_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda val: on_rgb_change())
rgb_b_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda val: on_rgb_change())
rgb_r_scale.grid(row=4, column=4, padx=5, pady=5)
rgb_g_scale.grid(row=4, column=5, padx=5, pady=5)
rgb_b_scale.grid(row=4, column=6, padx=5, pady=5)

def sync_scales_from_entries():
    try:
        r = int(rgb_r_entry.get())
        g = int(rgb_g_entry.get())
        b = int(rgb_b_entry.get())
        rgb_r_scale.set(r)
        rgb_g_scale.set(g)
        rgb_b_scale.set(b)
    except ValueError:
        pass

    try:
        l = float(lab_l_entry.get())
        a = float(lab_a_entry.get())
        b_val = float(lab_b_entry.get())
        lab_l_scale.set(l)
        lab_a_scale.set(a)
        lab_b_scale.set(b_val)
    except ValueError:
        pass

    try:
        x = float(xyz_x_entry.get())
        y = float(xyz_y_entry.get())
        z = float(xyz_z_entry.get())
        xyz_x_scale.set(x)
        xyz_y_scale.set(y)
        xyz_z_scale.set(z)
    except ValueError:
        pass

for i in range(7):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
