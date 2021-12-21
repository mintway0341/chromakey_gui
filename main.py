#https://github.com/mintway0341/chromakey_gui
#크기가 같은 배경 이미지와 크로마키 이미지(초록 또는 파랑)를 불러오면 합성을 해주는 GUI 프로그램입니다.
#초록색 크로마키와 파란색 크로마키를 모두 지원하며, 라디오 버튼으로 선택할 수 있습니다.
#크로마키 효과를 위해 배경 이미지에 블러 효과를 적용하였으며 사용자가 심도를 조절할 수 있습니다.
#Default 민감도로 합성된 이미지가 부자연스럽다면 사용자가 민감도를 조절할 수 있습니다.
#합성된 이미지를 저장하는 기능도 물론 구현되어 있습니다.

from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import cv2
import copy

isProcessed = False
file_bg = ""
file_chromakey = ""
blur_amount = 31
h_center = 60
h_sensitivity = 20
s_sensitivity = 50
v_sensitivity = 80
h_start = h_center - h_sensitivity
h_end = h_center + h_sensitivity
s_start = 200 - s_sensitivity * 2
s_end = 255
v_start = 200 - v_sensitivity * 2
v_end = 255
output_img = None


def add_file_bg():
    global file_bg
    file_bg = fd.askopenfilename(title="이미지를 선택하세요", \
                                        filetypes=(("png 파일", "*.png"), ("jpg 파일", "*.jpg"), ("jpeg 파일", "*.jpeg")), \
                                        initialdir=r"./")
    lbl_bg_path.config(text="배경 이미지 경로: " + file_bg)


def add_file_chromakey():
    global file_chromakey
    file_chromakey = fd.askopenfilename(title="이미지를 선택하세요", \
                                        filetypes=(("png 파일", "*.png"), ("jpg 파일", "*.jpg"), ("jpeg 파일", "*.jpeg")), \
                                        initialdir=r"./")
    lbl_chromakey_path.config(text="크로마키 이미지 경로: " + file_chromakey)


def process():
    global isProcessed
    global h_center
    global h_start
    global h_end
    h_center = rad_value.get()
    h_start = h_center - h_sensitivity
    h_end = h_center + h_sensitivity
    if file_bg != "" and file_chromakey != "":
        isProcessed = True
        background_bgr = cv2.imread(file_bg)
        chromakey_bgr = cv2.imread(file_chromakey)

        if background_bgr.shape[0] == chromakey_bgr.shape[0] and background_bgr.shape[1] == chromakey_bgr.shape[1]:
            if blur_amount != 0:
                background_blur = cv2.GaussianBlur(background_bgr, (blur_amount, blur_amount), 0)
            else:
                background_blur = copy.deepcopy(background_bgr)
            output = copy.deepcopy(background_blur)
            chromakey_hsv = cv2.cvtColor(chromakey_bgr, cv2.COLOR_BGR2HSV)
            mask = cv2.bitwise_not(cv2.inRange(chromakey_hsv, (h_start, s_start, v_start), (h_end, s_end, v_end)))
            cv2.copyTo(chromakey_bgr, mask, output)

            output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

            global output_img
            output_img = Image.fromarray(output_rgb)
            width, height = output_img.size
            output_resize = output_img.resize((500, round(500 / width * height)))
            output_imgtk = ImageTk.PhotoImage(image=output_resize)
            lbl_img.config(image=output_imgtk)
            lbl_img.image = output_imgtk

        else:
            isProcessed = False
            mb.showinfo("경고", "두 이미지의 크기를 통일해주세요")

    else:
        isProcessed = False
        mb.showinfo("경고", "이미지를 선택해주세요")


def slider1_changed(event):
    slider1_val = slider1.get()
    global blur_amount
    if slider1_val != 0:
        blur_amount = (slider1_val // 2) * 2 + 1
    else:
        blur_amount = 0

    global isProcessed
    if isProcessed:
        process()


def slider2_changed(event):
    slider2_val = slider2.get()
    global h_sensitivity
    global h_start
    global h_end
    h_sensitivity = slider2_val
    h_start = h_center - h_sensitivity
    h_end = h_center + h_sensitivity

    global isProcessed
    if isProcessed:
        process()


def slider3_changed(event):
    slider3_val = slider3.get()
    global s_sensitivity
    global s_start
    s_sensitivity = slider3_val
    s_start = 200 - s_sensitivity * 2

    global isProcessed
    if isProcessed:
        process()


def slider4_changed(event):
    slider4_val = slider4.get()
    global v_sensitivity
    global v_start
    v_sensitivity = slider4_val
    v_start = 200 - v_sensitivity * 2

    global isProcessed
    if isProcessed:
        process()


def reset1():
    slider1.set(31)


def reset2():
    slider2.set(20)


def reset3():
    slider3.set(50)


def reset4():
    slider4.set(80)


def save():
    filename = fd.asksaveasfile(mode="w", defaultextension=".jpg")
    process()
    if not filename:
        mb.showinfo("경고", "경로를 제대로 선택해주세요")
    elif isProcessed:
        output_img.save(filename)


root = Tk()
root.title("크로마키 합성")
root.geometry("1000x1200")
root.resizable(True, True)
frame_btn = Frame(root)
frame_btn.pack()
btn_add_file_bg = Button(frame_btn, padx=5, pady=5, width=12, text="배경 이미지 선택", command=add_file_bg)
btn_add_file_bg.pack(side="left")
btn_add_file_chromakey = Button(frame_btn, padx=5, pady=5, width=12, text="크로마키 이미지 선택", command=add_file_chromakey)
btn_add_file_chromakey.pack(side="right")

lbl_bg_path = Label(root, text="배경 이미지 경로: ")
lbl_bg_path.pack()
lbl_chromakey_path = Label(root, text="크로마키 이미지 경로: ")
lbl_chromakey_path.pack()

rad_value = IntVar()
rad_green = Radiobutton(root, text="초록색 크로마키", variable=rad_value, value=60)
rad_green.pack()
rad_blue = Radiobutton(root, text="파란색 크로마키", variable=rad_value, value=120)
rad_blue.pack()

rad_value.set(60)

frame_1 = Frame(root)
frame_1.pack()
slider1_value = IntVar()
slider1 = Scale(frame_1, label="배경블러 심도", variable=slider1_value, command=slider1_changed, orient="horizontal", showvalue=False, length=300)
slider1.set(31)
slider1.pack(side="left")
btn_reset1 = Button(frame_1, pady=2, width=3, text="초기화", command=reset1)
btn_reset1.pack(side="right")

frame_2 = Frame(root)
frame_2.pack()
slider2_value = IntVar()
slider2 = Scale(frame_2, label="H 민감도", variable=slider2_value, command=slider2_changed, orient="horizontal", showvalue=False, length=300)
slider2.set(20)
slider2.pack(side="left")
btn_reset2 = Button(frame_2, pady=2, width=3, text="초기화", command=reset2)
btn_reset2.pack(side="right")

frame_3 = Frame(root)
frame_3.pack()
slider3_value = IntVar()
slider3 = Scale(frame_3, label="S 민감도", variable=slider3_value, command=slider3_changed, orient="horizontal", showvalue=False, length=300)
slider3.set(50)
slider3.pack(side="left")
btn_reset3 = Button(frame_3, pady=2, width=3, text="초기화", command=reset3)
btn_reset3.pack(side="right")

frame_4 = Frame(root)
frame_4.pack()
slider4_value = IntVar()
slider4 = Scale(frame_4, label="V 민감도", variable=slider4_value, command=slider4_changed, orient="horizontal", showvalue=False, length=300)
slider4.set(80)
slider4.pack(side="left")
btn_reset4 = Button(frame_4, pady=2, width=3, text="초기화", command=reset4)
btn_reset4.pack(side="right")

frame_process_save = Frame(root)
frame_process_save.pack()
btn_add_file_chromakey = Button(frame_process_save, pady=5, width=5, text="합성", command=process)
btn_add_file_chromakey.pack(side="left")
btn_save = Button(frame_process_save, pady=5, width=5, text="저장", command=save)
btn_save.pack(side="right")

lbl_img = Label(root)
lbl_img.pack()

root.mainloop()
