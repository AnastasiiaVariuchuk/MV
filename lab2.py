import glfw
from OpenGL.GL import *
from tkinter import *
import numpy as np
from math import sqrt, atan2, pi

circle_radius = 0.25
circle_center_x = 0.5
circle_center_y = 0.5
pixel_connectivity = 4  # Зв'язність у 4 пікселі

# Вікно розміром 800x800
width, height = 800, 800


def draw_circle_with_pixel_connectivity(radius, pixel_connectivity, window_size):
    # Обчислюємо довжину кола
    circumference = 2 * pi * radius
    # Обчислюємо кількість сегментів для зв'язності
    segment_length = pixel_connectivity / window_size  # Довжина сегменту відносно вікна
    segments = int(circumference / segment_length)  # Обчислюємо кількість сегментів

    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * pi * i / segments
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        glVertex2f(x, y)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # glScalef(8.0, 8.0, 1.0)

    # Зміна масштабу для осей (додаємо більше простору навколо координат)
    glOrtho(0, 1.5, 0, 1.5, -1, 1)

    # Малювання координатних осей
    glColor3f(0, 0, 1)
    glBegin(GL_LINES)
    glVertex2f(1, 1)
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glEnd()

    # Малювання кола з урахуванням зв'язності у 4 пікселі
    glColor3f(0, 1, 0)
    glPushMatrix()
    glTranslatef(1 - circle_center_x, 1 - circle_center_y, 0)  # Переміщення центру з урахуванням зміщення координат
    draw_circle_with_pixel_connectivity(circle_radius, pixel_connectivity, width)
    glPopMatrix()


def glfw_main_loop(window):
    """ Обробка рендерингу для GLFW """
    if not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()
        root.after(10, glfw_main_loop, window)
    else:
        glfw.terminate()


def start_glfw_render():
    """ Функція для запуску рендерингу через GLFW """
    if not glfw.init():
        return

    window = glfw.create_window(width, height, "OpenGL Circle", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    root.after(10, glfw_main_loop, window)


def convert_to_cylindrical(x, y):
    """ Переведення декартових координат у циліндричні """
    r = sqrt(x ** 2 + y ** 2)
    theta = atan2(y, x)  # Кут у радіанах
    if theta < 0:
        theta += 2 * pi
    return r, theta


def on_submit():
    """ Обробник натискання кнопки для введення нових значень кола """
    global circle_radius, circle_center_x, circle_center_y

    try:
        circle_radius = float(radius_entry.get())
        circle_center_x = float(center_x_entry.get())
        circle_center_y = float(center_y_entry.get())

        # Переведення у циліндричну систему координат
        r, theta = convert_to_cylindrical(circle_center_x, circle_center_y)

        result_label.config(text=f"Циліндричні координати: r = {r:.2f}, θ = {theta:.2f} радіан")
    except ValueError:
        result_label.config(text="Невірний формат введення")


def create_gui():
    """ Функція для створення графічного інтерфейсу користувача з використанням Tkinter """
    global radius_entry, center_x_entry, center_y_entry, result_label, root

    root = Tk()
    root.title("Параметри кола")

    Label(root, text="Радіус кола:").grid(row=0, column=0, padx=10, pady=5)
    radius_entry = Entry(root)
    radius_entry.grid(row=0, column=1, padx=10, pady=5)
    radius_entry.insert(0, "0.25")

    Label(root, text="Координата X центру:").grid(row=1, column=0, padx=10, pady=5)
    center_x_entry = Entry(root)
    center_x_entry.grid(row=1, column=1, padx=10, pady=5)
    center_x_entry.insert(0, "0.5")

    Label(root, text="Координата Y центру:").grid(row=2, column=0, padx=10, pady=5)
    center_y_entry = Entry(root)
    center_y_entry.grid(row=2, column=1, padx=10, pady=5)
    center_y_entry.insert(0, "0.5")

    submit_button = Button(root, text="Підтвердити", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    result_label = Label(root, text="Циліндричні координати з'являться тут")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    start_glfw_render()
    root.mainloop()


create_gui()