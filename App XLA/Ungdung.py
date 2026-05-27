from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import cv2
import numpy as np
from PIL import Image, ImageTk
from scipy.ndimage import filters
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# import matplotlib.pyplot as plt

class Application(Frame):

    def __init__(self):
        super().__init__()
        # global canvas_goc
        self.master.title("Nâng cao chất lượng ảnh")
        self.pack()
        menubar = Menu(self.master)
        # Menu
        # Chức năng
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Mở ảnh", command=self.make_image)

        filemenu.add_separator()
        filemenu.add_command(label="Thoát", command=self.master.destroy)
        menubar.add_cascade(label="Chức năng", menu=filemenu)

        # Chức năng About
        aboutmenu = Menu(menubar, tearoff=0)
        aboutmenu.add_command(label="Nhóm thực hiện", command=self.nhomthuchien)
        aboutmenu.add_command(label="Ứng dụng", command=self.ungdung)
        menubar.add_cascade(label="Giới thiệu", menu=aboutmenu)

        # Chức năng Help
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Hướng dẫn sử dụng phần mềm", command=self.hdsd)
        menubar.add_cascade(label="Trợ giúp", menu=helpmenu)
        # //Help
        self.master.config(menu=menubar)
        # //Menu
        # top
        frame = Frame(self.master)
        frame.pack()
        self.label_tieude = Label(frame, pady=20, text="NÂNG CAO CHẤT LƯỢNG ẢNH SỬ DỤNG THƯ VIỆN OPENCV", fg="red",
                                  font=("Helvetica", 18), padx=20)
        self.label_tieude.pack()
        # //top

        # middle
        middleframe = Frame(self.master, padx=10)
        middleframe.pack()
        # Chọn thông số
        middleframe_1 = Frame(middleframe, padx=10)
        middleframe_1.pack(fill=Y, side=LEFT)
        self.middleframe_1_1 = Frame(middleframe_1, bd=1, relief="solid", pady=214, padx=20)
        self.middleframe_1_1.pack()

        #Nút mở ảnh
        openbutton = Button(self.middleframe_1_1, text="Mở ảnh", bg="#42f4c5", fg="black", command=self.make_image)
        openbutton.pack()

        cbbChucnang_frame = Frame(self.middleframe_1_1, pady=10)
        cbbChucnang_frame.pack()
        self.chucnang_value = StringVar()
        self.combo_chucnang = Combobox(cbbChucnang_frame, textvariable=self.chucnang_value, state=DISABLED)
        self.combo_chucnang.set("Chọn chức năng")
        self.combo_chucnang["value"] = ["Xoay ảnh", "Lọc ảnh", "Tách biên"]
        self.combo_chucnang.pack()
        self.combo_chucnang.bind("<<ComboboxSelected>>", self.getChucnang)

        self.gocxoay = IntVar()
        self.xoayanhframe_1 = Frame(self.middleframe_1_1, bd=1, relief="solid")
        self.xoayanhframe_1.pack_forget()
        tsxoayanh_frame = Frame(self.xoayanhframe_1, bd=1, relief="solid")
        tsxoayanh_frame.pack()
        label_d0 = Label(tsxoayanh_frame, text="radius:", font=("Helvetica", 10), pady=20)
        label_d0.pack(fill=Y, side=LEFT)
        self.top = Scale(tsxoayanh_frame, from_=0, to=359, variable=self.gocxoay, orient=HORIZONTAL).pack(fill=Y, side=LEFT)

        self.locanhframe_1 = Frame(self.middleframe_1_1, bd=1, relief="solid")
        self.locanhframe_1.pack_forget()
        thongso_frame_1 = Frame(self.locanhframe_1, bd=1, relief="solid")
        thongso_frame_1.pack()

        self.var = IntVar()
        self.ksize_gau = IntVar()
        self.ksize_median = IntVar()
        self.d_bila = IntVar()
        self.sigma_bila = IntVar()
        self.ksize_box = IntVar()
        self.ksize_2d = IntVar()
        label_boloc = Label(thongso_frame_1, text="Lọc theo hàm", font=("Helvetica", 10))
        label_boloc.pack()
        self.hamloc_value = StringVar()
        self.combo_1 = Combobox(thongso_frame_1, textvariable=self.hamloc_value,
                                value=["GaussianFilter", "MedianFilter", "BilateralFilter", "BoxFilter", "2DFilter"],
                                state=DISABLED)
        self.combo_1.set("Chọn hàm lọc")
        self.combo_1.pack()
        self.combo_1.bind("<<ComboboxSelected>>", self.getHamloc)
        """
        self.tssobel_frame=Frame(thongso_frame_1)
        self.tssobel_frame.pack_forget()
        label_d0 = Label(self.tssobel_frame, text="axis:",font=("Helvetica", 10),pady=20)
        label_d0.pack(fill=Y,side=LEFT)
        self.top = Scale(self.tssobel_frame,from_=0,to=1,variable = self.var, orient = HORIZONTAL).pack(fill=Y,side=LEFT)
        """
        self.past = 1
        self.tsgausian_frame = Frame(thongso_frame_1)
        self.tsgausian_frame.pack_forget()
        label_d1 = Label(self.tsgausian_frame, text="ksize:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_gau = Scale(self.tsgausian_frame, from_=1, to=199, variable=self.ksize_gau, orient=HORIZONTAL,
                               command=self.selto_gau)
        self.scale_gau.pack(fill=Y, side=LEFT)

        self.tsmedianfilter_frame = Frame(thongso_frame_1)
        self.tsmedianfilter_frame.pack_forget()
        label_d1 = Label(self.tsmedianfilter_frame, text="ksize:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scalemedian = Scale(self.tsmedianfilter_frame, from_=3, to=199, variable=self.ksize_median,
                                 orient=HORIZONTAL, command=self.selto_median)
        self.scalemedian.pack(fill=Y, side=LEFT)

        self.tsbila_filter_frame = Frame(thongso_frame_1)
        self.tsbila_filter_frame.pack_forget()
        self.tsbila_filter_frame1 = Frame(self.tsbila_filter_frame)
        self.tsbila_filter_frame1.pack(fill=X)
        label_d1 = Label(self.tsbila_filter_frame1, text="d:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_bila_d = Scale(self.tsbila_filter_frame1, from_=1, to=99, variable=self.d_bila, orient=HORIZONTAL,
                                  command=self.selto_bila_d)
        self.scale_bila_d.pack(fill=Y, side=RIGHT)
        self.tsbila_filter_frame2 = Frame(self.tsbila_filter_frame)
        self.tsbila_filter_frame2.pack(fill=X)
        label_d1 = Label(self.tsbila_filter_frame2, text="sigma:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_bila_sigma = Scale(self.tsbila_filter_frame2, from_=1, to=999, variable=self.sigma_bila,
                                      orient=HORIZONTAL, command=self.selto_bila_sigma)
        self.scale_bila_sigma.pack(fill=Y, side=RIGHT)

        self.tsboxfilter_frame = Frame(thongso_frame_1)
        self.tsboxfilter_frame.pack_forget()
        label_d1 = Label(self.tsboxfilter_frame, text="size:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_box = Scale(self.tsboxfilter_frame, from_=1, to=250, variable=self.ksize_box, orient=HORIZONTAL)
        self.scale_box.pack(fill=Y, side=LEFT)

        self.ts2dfilter_frame = Frame(thongso_frame_1)
        self.ts2dfilter_frame.pack_forget()
        label_d1 = Label(self.ts2dfilter_frame, text="size:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_2d = Scale(self.ts2dfilter_frame, from_=1, to=250, variable=self.ksize_2d, orient=HORIZONTAL)
        self.scale_2d.pack(fill=Y, side=LEFT)

        label_kenhmau = Label(thongso_frame_1, text="Tách theo kênh màu", font=("Helvetica", 10))
        label_kenhmau.pack()
        self.kenhmau_value = StringVar()
        self.combo_2 = Combobox(thongso_frame_1, textvariable=self.kenhmau_value, state=DISABLED)
        self.combo_2.set("RGB")
        self.combo_2["value"] = ["RGB", "Red", "Green", "Blue"]
        self.combo_2.pack()
        self.label_rad = Label(thongso_frame_1)
        self.label_rad.pack()
        self.combo_2.bind("<<ComboboxSelected>>", self.getKenhmau)

        # tach bien
        self.tachbienframe_1 = Frame(self.middleframe_1_1, bd=1, relief="solid")
        self.tachbienframe_1.pack_forget()
        thongso_frame_2 = Frame(self.tachbienframe_1, bd=1, relief="solid")
        thongso_frame_2.pack()

        self.ksize_sobel = IntVar()
        self.ksize_laplac = IntVar()

        #Combobox chọn hàm tách biên
        label_tachbien = Label(thongso_frame_2, text="Tách biên theo hàm", font=("Helvetica", 10))
        label_tachbien.pack()
        self.hamtachbien_value = StringVar()
        self.combo_tachbien = Combobox(thongso_frame_2, textvariable=self.hamtachbien_value,
                                       value=["Sobel", "Laplacian"], state=DISABLED)
        self.combo_tachbien.set("Chọn hàm tách biên")
        self.combo_tachbien.pack()
        self.combo_tachbien.bind("<<ComboboxSelected>>", self.getTachbien)
        """
        self.tssobel_frame=Frame(thongso_frame_1)
        self.tssobel_frame.pack_forget()
        label_d0 = Label(self.tssobel_frame, text="axis:",font=("Helvetica", 10),pady=20)
        label_d0.pack(fill=Y,side=LEFT)
        self.top = Scale(self.tssobel_frame,from_=0,to=1,variable = self.var, orient = HORIZONTAL).pack(fill=Y,side=LEFT)
        """
        # Sobel Ddepth độ sâu
        self.tssobel_frame = Frame(thongso_frame_2)
        self.tssobel_frame.pack_forget()
        self.combosb_frame = Frame(self.tssobel_frame)
        self.combosb_frame.pack(fill=X)
        self.hamdosau_value = StringVar()
        label_dosau = Label(self.combosb_frame, text="Ddepth", font=("Helvetica", 10))
        label_dosau.pack()
        self.combo_ddepth = Combobox(self.combosb_frame, textvariable=self.hamdosau_value,
                                     value=["CV_8U", "CV_16U", "CV_32F"], state=DISABLED)
        self.combo_ddepth.set("CV_8U")
        self.combo_ddepth.pack()

        #Chọn hướng đạo hàm("<<ComboboxSelected>>", self.getDosau)
        self.radiosb_frame = Frame(self.tssobel_frame)
        self.radiosb_frame.pack(fill=X)
        label_dxy = Label(self.radiosb_frame, text="(dx,dy):", font=("Helvetica", 10))
        label_dxy.pack(side=LEFT, fill=Y)
        self.radio_dxy = IntVar()
        self.radio_dxy.set(2)
        R1 = Radiobutton(self.radiosb_frame, text="(1,0)", variable=self.radio_dxy, value=1)
        R1.pack(fill=Y, side=RIGHT)
        R2 = Radiobutton(self.radiosb_frame, text="(0,1)", variable=self.radio_dxy, value=2)
        R2.pack(fill=Y, side=RIGHT)

        #Kích thước kernel cho Sobel
        self.scalesb_frame = Frame(self.tssobel_frame)
        self.scalesb_frame.pack(fill=X)
        label_d1 = Label(self.scalesb_frame, text="ksize:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_sobel = Scale(self.scalesb_frame, from_=1, to=21, variable=self.ksize_sobel, orient=HORIZONTAL,
                                 command=self.selto_sobel)
        self.scale_sobel.pack(fill=Y, side=LEFT)

        # Laplacian
        self.tslaplac_frame = Frame(thongso_frame_2)
        self.tslaplac_frame.pack_forget()
        self.comboll_frame = Frame(self.tslaplac_frame)
        self.comboll_frame.pack(fill=X)
        self.hamdosau1_value = StringVar()
        label_dosau = Label(self.comboll_frame, text="Ddepth", font=("Helvetica", 10))
        label_dosau.pack()
        self.combo2_ddepth = Combobox(self.comboll_frame, textvariable=self.hamdosau1_value,
                                      value=["CV_8U", "CV_16U", "CV_32F"], state=DISABLED)
        self.combo2_ddepth.set("CV_8U")
        self.combo2_ddepth.pack()
        # self.combo2_ddepth.bind("<<ComboboxSelected>>", self.getDosau)

        self.scalell_frame = Frame(self.tslaplac_frame)
        self.scalell_frame.pack(fill=X)
        label_d1 = Label(self.scalell_frame, text="ksize:", font=("Helvetica", 10), pady=20)
        label_d1.pack(fill=Y, side=LEFT)
        self.scale_laplac = Scale(self.scalell_frame, from_=1, to=21, variable=self.ksize_laplac, orient=HORIZONTAL,
                                  command=self.selto_laplac)
        self.scale_laplac.pack(fill=Y, side=LEFT)

        label_kenhmau = Label(thongso_frame_2, text="Tách theo kênh màu", font=("Helvetica", 10))
        label_kenhmau.pack()
        self.kenhmau2_value = StringVar()
        self.combo_chanel = Combobox(thongso_frame_2, textvariable=self.kenhmau2_value, state=DISABLED)
        self.combo_chanel.set("Gray")
        self.combo_chanel["value"] = ["Gray", "Red", "Green", "Blue"]
        self.combo_chanel.pack()
        self.label_rad1 = Label(thongso_frame_2)
        self.label_rad1.pack()
        self.combo_chanel.bind("<<ComboboxSelected>>", self.getKenhmau)

        # ảnh gốc
        middleframe_2 = Frame(middleframe, bd=1, relief="solid")
        middleframe_2.pack()
        anhgoc_frame = Frame(middleframe_2, padx=5)
        anhgoc_frame.pack(fill=Y, side=LEFT)
        label = Label(anhgoc_frame, text="Ảnh gốc", font=("Helvetica", 12))
        label.pack()
        self.canvas_goc = Canvas(anhgoc_frame, height=210, width=200, bd=4, bg="#b8bdc4", relief="ridge")
        self.canvas_goc.pack()
        self.hisred_frame = Frame(middleframe_2, padx=5)
        self.hisred_frame.pack(fill=Y, side=LEFT)
        self.hisblue_frame = Frame(middleframe_2, padx=5)
        self.hisblue_frame.pack(fill=Y, side=LEFT)
        self.hisgreen_frame = Frame(middleframe_2, padx=5)
        self.hisgreen_frame.pack(fill=Y, side=LEFT)

        # ảnh xử lý
        middleframe_3 = Frame(middleframe, bd=1, relief="solid")
        middleframe_3.pack()
        anhxl_frame = Frame(middleframe_3, padx=5)
        anhxl_frame.pack(fill=Y, side=LEFT)
        label = Label(anhxl_frame, text="Ảnh xử lý", font=("Helvetica", 12))
        label.pack()
        self.canvas_xl = Canvas(anhxl_frame, height=210, width=200, bd=4, bg="#b8bdc4", relief="ridge")
        self.canvas_xl.pack()
        self.hisred_frame2 = Frame(middleframe_3, padx=5)
        self.hisred_frame2.pack(fill=Y, side=LEFT)
        self.hisblue_frame2 = Frame(middleframe_3, padx=5)
        self.hisblue_frame2.pack(fill=Y, side=LEFT)
        self.hisgreen_frame2 = Frame(middleframe_3, padx=5)
        self.hisgreen_frame2.pack(fill=Y, side=LEFT)

        bottomframe = Frame(self.master, pady=20)
        bottomframe.pack()
        bottomframe_1 = Frame(bottomframe, padx=20)
        bottomframe_1.pack(side=LEFT)
        self.redbutton = Button(bottomframe_1, text="Xử lý", state=DISABLED, fg="black", padx=20, command=self.locanh)
        self.redbutton.pack()
        bottomframe_3 = Frame(bottomframe, padx=20)
        bottomframe_3.pack(side=LEFT)
        self.bluebutton = Button(bottomframe_3, text="Xoay ảnh", state=DISABLED, fg="black", padx=20,
                                 command=self.xoayanh)
        self.bluebutton.pack()
        bottomframe_2 = Frame(bottomframe, padx=20)
        bottomframe_2.pack(side=LEFT)
        self.greenbutton = Button(bottomframe_2, text="Lưu", state=DISABLED, fg="black", padx=20, command=self.luuanh)
        self.greenbutton.pack()

        self.status = Label(self.master, text="Curent Image: None", bg="#b6b7ba", font=("", 13), relief="sunken", bd=2,
                            fg="black", anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

    def getKenhmau(self, event):
        self.redbutton["state"] = NORMAL
        self.redbutton["bg"] = "#c741f4"

    def getChucnang(self, event):
        self.bluebutton["state"] = NORMAL
        self.bluebutton["bg"] = "#d6ac42"

        if self.chucnang_value.get() == "Xoay ảnh":
            self.xoayanhframe_1.pack(fill=X)
            self.locanhframe_1.pack_forget()
            self.middleframe_1_1["pady"] = 179
            self.tachbienframe_1.pack_forget()
        if self.chucnang_value.get() == "Lọc ảnh":
            self.locanhframe_1.pack(fill=X)
            self.xoayanhframe_1.pack_forget()
            self.tachbienframe_1.pack_forget()
            self.bluebutton["state"] = DISABLED
            # self.bluebutton["bg"]=none
            self.middleframe_1_1["pady"] = 169
        if self.chucnang_value.get() == "Tách biên":
            self.tachbienframe_1.pack(fill=X)
            self.xoayanhframe_1.pack_forget()
            self.locanhframe_1.pack_forget()
            self.bluebutton["state"] = DISABLED
            self.middleframe_1_1["pady"] = 169

    def getHamloc(self, event):
        self.redbutton["state"] = NORMAL
        self.redbutton["bg"] = "#c741f4"
        self.combo_2["state"] = "readonly"

        if self.hamloc_value.get() == "GaussianFilter":
            self.combo_2.set("RGB")
            self.combo_2["value"] = ["RGB", "Red", "Green", "Blue"]
            self.tsgausian_frame.pack()
            self.middleframe_1_1["pady"] = 129
        else:
            self.combo_2.set("RGB")
            self.combo_2["value"] = ["RGB", "Red", "Green", "Blue"]
            self.tsgausian_frame.pack_forget()

        if self.hamloc_value.get() == "MedianFilter":
            self.tsmedianfilter_frame.pack()
            self.middleframe_1_1["pady"] = 129
        else:
            self.tsmedianfilter_frame.pack_forget()

        if self.hamloc_value.get() == "BilateralFilter":
            self.tsbila_filter_frame.pack()
            self.middleframe_1_1["pady"] = 99
        else:
            self.tsbila_filter_frame.pack_forget()

        if self.hamloc_value.get() == "BoxFilter":
            self.tsboxfilter_frame.pack()
            self.middleframe_1_1["pady"] = 129
        else:
            self.tsboxfilter_frame.pack_forget()

        if self.hamloc_value.get() == "2DFilter":
            self.ts2dfilter_frame.pack()
            self.middleframe_1_1["pady"] = 129
        else:
            self.ts2dfilter_frame.pack_forget()

    def getTachbien(self, event):
        self.redbutton["state"] = NORMAL
        self.redbutton["bg"] = "#c741f4"
        self.combo_chanel["state"] = "readonly"

        if self.hamtachbien_value.get() == "Sobel":
            self.combo_ddepth["state"] = "readonly" #cho phép chọn ddepth
            self.combo_chanel.set("Gray") #mặc định dùng ảnh Gray
            self.combo_chanel["value"] = ["Gray", "Red", "Green", "Blue"]
            self.tssobel_frame.pack()
            self.middleframe_1_1["pady"] = 69
        else:
            self.combo_chanel.set("Gray")
            self.combo_chanel["value"] = ["Gray", "Red", "Green", "Blue"]
            self.tssobel_frame.pack_forget()

        if self.hamtachbien_value.get() == "Laplacian":
            self.combo2_ddepth["state"] = "readonly"
            self.tslaplac_frame.pack()
            self.middleframe_1_1["pady"] = 99
        else:
            self.tslaplac_frame.pack_forget()

    """       
    def getDosau(self,event):
        print(self.hamdosau_value.get())
        #self.combo_chanel["state"]="readonly"
        if self.hamtachbien_value.get() =="Sobel": 
            self.tssobel_frame.pack()
            self.middleframe_1_1["pady"]=69
        else:
            self.tssobel_frame.pack_forget()

        if self.hamtachbien_value.get() =="Laplacian": 
            self.tslaplac_frame.pack()
            self.middleframe_1_1["pady"]=99
        else:
            self.tslaplac_frame.pack_forget()
    """
    #Kernel phải là số lẻ, nếu chăn thì tự động chỉnh lại
    def selto_median(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scalemedian.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scalemedian.get()

    def selto_gau(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scale_gau.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scale_gau.get()

    def selto_bila_d(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scale_bila_d.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scale_bila_d.get()

    def selto_bila_sigma(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scale_bila_sigma.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scale_bila_sigma.get()

    def selto_sobel(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scale_sobel.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scale_sobel.get()

    def selto_laplac(self, n):
        self.n = n
        self.n = int(self.n)
        if not self.n % 2:
            self.scale_laplac.set(self.n + 1 if self.n > self.past else self.n - 1)
            self.past = self.scale_laplac.get()

    def make_image(self):
        try:
            File = fd.askopenfilename(title="Chọn ảnh",
                                      filetype=[("jpeg", "*.jpg"), ("png", "*.png"), ("All files", "*")])
            self.img = cv2.imread(File)
            self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.height, self.width, self.depth = self.img.shape
            self.img_bathname = File
            self.a = self.img_bathname.split('/')
            self.name_img = self.a[len(self.a) - 1]
            self.im = Image.fromarray(self.img_rgb)

            #Resize + đưa ảnh vào canvas
            self.reimg = self.im.resize((200, 210), Image.Resampling.LANCZOS)
            self.tatras = ImageTk.PhotoImage(self.reimg)
            self.canvas_goc.delete("all")
            self.canvas_goc.create_image(10, 10, anchor=NW, image=self.tatras)
            self.canvas_goc.pack(fill=BOTH, expand=1)
            self.canvas_goc.bind("<Enter>", self.on_enter)
            self.canvas_goc.bind("<Leave>", self.on_leave)

            #Xóa histogram cũ
            for widget in self.hisgreen_frame.winfo_children():
                widget.pack_forget()
            for widget in self.hisblue_frame.winfo_children():
                widget.pack_forget()
            for widget in self.hisred_frame.winfo_children():
                widget.pack_forget()

            #Hiển thị Histogram mới
            label = Label(self.hisred_frame, text="Histogram Red", font=("Helvetica", 12))
            label.pack()
            figure1 = plt.figure(num=0, figsize=(4.1, 3.1), dpi=70)
            self.histred = cv2.calcHist([self.img], [2], None, [256], [0, 256])
            plt.plot(self.histred, color='r')
            self.canvas_goc_red = FigureCanvasTkAgg(figure1, self.hisred_frame)
            self.canvas_goc_red.get_tk_widget().pack()

            label = Label(self.hisgreen_frame, text="Histogram Green", font=("Helvetica", 12))
            label.pack()
            figure2 = plt.figure(num=1, figsize=(4.1, 3.1), dpi=70)
            self.histgreen = cv2.calcHist([self.img], [1], None, [256], [0, 256])
            plt.plot(self.histgreen, color='g')
            self.canvas_goc_green = FigureCanvasTkAgg(figure2, self.hisgreen_frame)
            self.canvas_goc_green.get_tk_widget().pack()

            label = Label(self.hisblue_frame, text="Histogram Blue", font=("Helvetica", 12))
            label.pack()
            figure3 = plt.figure(num=2, figsize=(4.1, 3.1), dpi=70)
            self.histblue = cv2.calcHist([self.img], [0], None, [256], [0, 256])
            plt.plot(self.histblue, color='b')
            self.canvas_goc_blue = FigureCanvasTkAgg(figure3, self.hisblue_frame)
            self.canvas_goc_blue.get_tk_widget().pack()
            plt.close('all')
            self.combo_1["state"] = "readonly"
            self.combo_chucnang["state"] = "readonly"
            self.combo_tachbien["state"] = "readonly"
        except:
            print("Chưa chọn ảnh")

    def xoayanh(self):
        self.greenbutton["state"] = NORMAL
        self.greenbutton["bg"] = "#7685f2"
        (h, w) = self.img.shape[:2]

        #Tạo ma trận xoay quanh tâm ảnh và áp ma trận affine để xoay. Kích thước output giữ nguyên (w,h).
        M = cv2.getRotationMatrix2D((w / 2, h / 2), self.gocxoay.get(), 1)
        self.xoayanhfilter = cv2.warpAffine(self.img, M, (w, h))
        cv2.imwrite("sobel.jpg", self.xoayanhfilter)
        self.save_img = self.xoayanhfilter
        self.sobel_img = cv2.imread("sobel.jpg")

        #Chuyển BGR->RGB để hiển thị bằng Tkinter, resize để khớp canvas, tạo PhotoImage và vẽ lên Canvas.
        self.img_rgb2 = cv2.cvtColor(self.sobel_img, cv2.COLOR_BGR2RGB)
        self.im2 = Image.fromarray(self.img_rgb2)
        self.reimg_2 = self.im2.resize((200, 210), Image.Resampling.LANCZOS)
        self.tatras_2 = ImageTk.PhotoImage(self.reimg_2)
        self.canvas_xl.delete("all")
        self.canvas_xl.create_image(10, 10, anchor=NW, image=self.tatras_2)
        self.canvas_xl.pack(fill=BOTH, expand=1)

        #Ẩn histogram ảnh xử lý (bạn ẩn để không hiển thị khi chưa cập nhật histogram cho ảnh xoay)
        self.hisred_frame2.pack_forget()
        self.hisblue_frame2.pack_forget()
        self.hisgreen_frame2.pack_forget()

    def luuanh(self):

        file = fd.asksaveasfilename(title="Lưu ảnh",
                                    filetype=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("All files", "*.*")))
        if file:
            # self.save_img.save(file)
            cv2.imwrite(file, self.save_img)

    def locanh(self):
        self.hisred_frame2.pack(fill=Y, side=LEFT)
        self.hisblue_frame2.pack(fill=Y, side=LEFT)
        self.hisgreen_frame2.pack(fill=Y, side=LEFT)
        self.greenbutton["state"] = NORMAL
        self.greenbutton["bg"] = "#7685f2"
        if self.hamloc_value.get() == "GaussianFilter":
            #(ksize, ksize) cần là số lẻ và >=1; sigma 0 để OpenCV tính sigma tự động.
            self.gau_blur = cv2.GaussianBlur(self.img, (self.ksize_gau.get(), self.ksize_gau.get()), 0)
            # cv2.imshow('',self.gau_blur)
            self.xulychung(self.gau_blur)

        if self.hamloc_value.get() == "MedianFilter":
            self.median_filter = cv2.medianBlur(self.img, self.ksize_median.get()) #ksize phải là số lẻ >=3 (OpenCV yêu cầu).
            self.xulychung(self.median_filter)

        if self.hamloc_value.get() == "BilateralFilter":
            self.bilafilter = cv2.bilateralFilter(self.img, self.d_bila.get(), self.sigma_bila.get(),
                                                  self.sigma_bila.get())
            self.xulychung(self.bilafilter)

        if self.hamloc_value.get() == "BoxFilter":
            self.boxfilter = cv2.boxFilter(self.img, -1, (self.ksize_box.get(), self.ksize_box.get())) #ddepth=-1 giữ cùng loại ảnh như input.
            self.xulychung(self.boxfilter)

        if self.hamloc_value.get() == "2DFilter":
            #  Tạo kernel trung bình (mean filter). Nếu ksize_2d chẵn, có thể vẫn chạy nhưng thường muốn lẻ.
            kernel = np.ones((self.ksize_2d.get(), self.ksize_2d.get()), np.float32) / (
                        self.ksize_2d.get() * self.ksize_2d.get())
            self.haidfilter = cv2.filter2D(self.img, -1, kernel)
            self.xulychung(self.haidfilter)
        if self.hamtachbien_value.get() == "Sobel":
            if self.hamdosau_value.get() == "CV_8U":
                self.delph = cv2.CV_8U
            if self.hamdosau_value.get() == "CV_16U":
                self.delph = cv2.CV_16U
            if self.hamdosau_value.get() == "CV_32F":
                self.delph = cv2.CV_32F
            if self.radio_dxy.get() == 1:
                self.dx = 1
                self.dy = 0
            if self.radio_dxy.get() == 2:
                self.dx = 0
                self.dy = 1
            #ksize cho Sobel phải là 1 hoặc lẻ >=3. Đảm bảo selto_sobel đã ép số lẻ (bạn đã có hàm selto_sobel).
            self.sobel = cv2.Sobel(self.img, self.delph, self.dx, self.dy, ksize=self.ksize_sobel.get())
            self.xulychung_tachbien(self.sobel)

        if self.hamtachbien_value.get() == "Laplacian":
            if self.hamdosau1_value.get() == "CV_8U":
                self.delph1 = cv2.CV_8U
            if self.hamdosau1_value.get() == "CV_16U":
                self.delph1 = cv2.CV_16U
            if self.hamdosau1_value.get() == "CV_32F":
                self.delph1 = cv2.CV_32F
            self.laplac = cv2.Laplacian(self.img, self.delph1, ksize=self.ksize_laplac.get())
            self.xulychung_tachbien(self.laplac)

    def xulycon(self):
        self.sobel_img = Image.open("sobel.jpg")
        self.img_gau = cv2.imread("sobel.jpg")

        #Chuyển BGR → RGB để tạo PIL image, resize, tạo PhotoImage và hiển thị lên canvas.
        self.img_rgb2 = cv2.cvtColor(self.img_gau, cv2.COLOR_BGR2RGB)
        self.im2 = Image.fromarray(self.img_rgb2)
        self.reimg2 = self.im2.resize((200, 210), Image.Resampling.LANCZOS)
        self.tatras2 = ImageTk.PhotoImage(self.reimg2) #Lưu self.tatras2 (tham chiếu) rất quan trọng — nếu không giữ, ảnh có thể biến mất.
        self.canvas_xl.delete("all")
        self.canvas_xl.create_image(10, 10, anchor=NW, image=self.tatras2)
        self.canvas_xl.pack(fill=BOTH, expand=1)
        for widget in self.hisgreen_frame2.winfo_children():
            widget.pack_forget()
        for widget in self.hisblue_frame2.winfo_children():
            widget.pack_forget()
        for widget in self.hisred_frame2.winfo_children():
            widget.pack_forget()

        #Xóa nội dung cũ của khung histogram, tạo label.
        label = Label(self.hisred_frame2, text="Histogram Red", font=("Helvetica", 12))
        label.pack()
        figure4 = plt.figure(num=0, figsize=(4.1, 3.1), dpi=70)

        #Dùng cv2.calcHist([self.img_gau], [2], ...) để tính histogram kênh index 2 (ở OpenCV: BGR → 0=Blue,1=Green,2=Red) → OK.
        self.histred2 = cv2.calcHist([self.img_gau], [2], None, [256], [0, 256])
        plt.plot(self.histred2, color='r')
        self.canvas_xl_red = FigureCanvasTkAgg(figure4, self.hisred_frame2)
        self.canvas_xl_red.get_tk_widget().pack()

        label = Label(self.hisgreen_frame2, text="Histogram Green", font=("Helvetica", 12))
        label.pack()
        figure5 = plt.figure(num=1, figsize=(4.1, 3.1), dpi=70)
        self.histgreen = cv2.calcHist([self.img_gau], [1], None, [256], [0, 256])

        #Dùng matplotlib plt.plot(...) rồi nhúng FigureCanvasTkAgg.
        plt.plot(self.histgreen, color='g')
        self.canvas_xl_green = FigureCanvasTkAgg(figure5, self.hisgreen_frame2)
        self.canvas_xl_green.get_tk_widget().pack()

        label = Label(self.hisblue_frame2, text="Histogram Blue", font=("Helvetica", 12))
        label.pack()
        figure6 = plt.figure(num=2, figsize=(4.1, 3.1), dpi=70)
        self.histblue = cv2.calcHist([self.img_gau], [0], None, [256], [0, 256])
        plt.plot(self.histblue, color='b')
        self.canvas_xl_blue = FigureCanvasTkAgg(figure6, self.hisblue_frame2)
        self.canvas_xl_blue.get_tk_widget().pack()
        plt.close('all')

    def xulychung(self, s):
        #Copy ảnh đầu vào s (thường là numpy array BGR).
        self.s = s
        self.chanel = self.s.copy()

        #Ở OpenCV kênh 0=Blue,1=Green,2=Red; code này zero kênh 0 & 1 để chỉ còn kênh 2 (Red) → đúng
        if self.kenhmau_value.get() == "Red":
            self.chanel[:, :, 0] = 0
            self.chanel[:, :, 1] = 0
        if self.kenhmau_value.get() == "Blue":
            self.chanel[:, :, 1] = 0
            self.chanel[:, :, 2] = 0
        if self.kenhmau_value.get() == "Green":
            self.chanel[:, :, 0] = 0
            self.chanel[:, :, 2] = 0

        #Ghi file tạm 'sobel.jpg' rồi gán self.save_img để lưu cuối cùng, gọi xulycon() để hiển thị và vẽ histogram.
        cv2.imwrite('sobel.jpg', self.chanel)
        self.save_img = self.chanel
        self.xulycon()

    def xulychung_tachbien(self, s):
        self.s = s
        self.chanel_tachbien = self.s.copy()

        #Nếu chọn Gray, mảng 2D (single-channel) được tạo
        if self.kenhmau2_value.get() == "Gray":
            self.chanel_tachbien = cv2.cvtColor(self.chanel_tachbien, cv2.COLOR_BGR2GRAY)
        if self.kenhmau2_value.get() == "Red":
            self.chanel_tachbien[:, :, 0] = 0
            self.chanel_tachbien[:, :, 1] = 0
        if self.kenhmau2_value.get() == "Blue":
            self.chanel_tachbien[:, :, 1] = 0
            self.chanel_tachbien[:, :, 2] = 0
        if self.kenhmau2_value.get() == "Green":
            self.chanel_tachbien[:, :, 0] = 0
            self.chanel_tachbien[:, :, 2] = 0
        #sau khi convert về Gray, mảng có shape (h,w) — không còn 3 kênh, mà xulycon() tiếp tục tính histogram cho channels [2],[1],[0] → sẽ báo lỗi hoặc cho kết quả sai.
        cv2.imwrite('sobel.jpg', self.chanel_tachbien)
        self.save_img = self.chanel_tachbien
        self.xulycon()

    def on_enter(self, event):

        #Đây là callback khi con trỏ chuột vào canvas_goc
        self.status.configure(
            text="Tên ảnh:" + str(self.name_img) + ", Kích thước: (" + str(self.width) + "," + str(self.height) + " )") #Dòng lệnh cập nhật text với tên ảnh và kích thước (width, height) — các thuộc tính này được thiết lập khi người dùng chọn ảnh (make_image).

    def on_leave(self, enter):

        #Callback khi chuột rời canvas. Xóa text status.
        self.status.configure(text="")

    def hdsd(self):
        filewin = Toplevel(self.master)
        filewin.title("Hướng dẫn sử dụng")
        Label(filewin, fg="red", text="HƯỚNG DẪN SỬ DỤNG PHẦN MỀM", height="1", font=("Helvetica", 17), padx=200).pack()
        Label(filewin, anchor="w", text="Bước 1: Chọn ảnh", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- Cách 1: Nhấp chuột vào nút "Mở ảnh"', padx=30, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- Cách 2: Chức năng => Mở ảnh', padx=30, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w",
              text='Xuất hiện hộp thoại “Chọn ảnh”, tìm đến thư mục lưu ảnh sau đó douple click vào ảnh muốn chọn.',
              padx=30, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text="Bước 2: Chọn chức năng", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='Chọn "Xoay ảnh" nếu muốn xoay ảnh hoặc chọn "Lọc ảnh" nếu muốn lọc ảnh',
              padx=30, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text="Bước 3:", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- Nếu chọn Xoay ảnh:', padx=30, height="1", font=("Helvetica", 14)).pack(
            fill=X)
        Label(filewin, anchor="w", text='+ Chọn thông số "radius" tương ứng với số góc muốn xoay ảnh:', padx=50,
              height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Chọn nút "Xoay ảnh" để thu được ảnh xoay ', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- Nếu chọn lọc ảnh:', padx=30, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Sẽ có 5 bộ lọc, chọn 1 trong 5:', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w",
              text='- GaussianFilter: là một phương pháp làm mờ ảnh (blur) dựa trên phân phối chuẩn – Gaussian distribution.',
              padx=70, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- MedianFilter: là một bộ lọc phi tuyến dùng để lọc nhiễu Salt & Pepper.',
              padx=70, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='- BilateralFilter: là một bộ lọc làm mờ ảnh nhưng vẫn giữ cạnh rất tốt.',
              padx=70, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w",
              text='- BoxFilter: (MeanFilter) là một bộ lọc làm mờ trung bình rất đơn giản trong xử lý ảnh.', padx=70,
              height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w",
              text='- 2DFilter: trong xử lý ảnh là bất kỳ bộ lọc nào sử dụng ma trận kernel 2D để tích chập (convolution) với ảnh',
              padx=70, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w",
              text='+ Chọn thông số cho bộ lọc: Mỗi bộ lọc đều có thông số tương ứng, điều chỉnh các thông số theo ý muốn',
              padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Chọn nút "Lọc ảnh" để thu được ảnh sau khi lọc', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text="Bước 4:", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='Chọn nút “Lưu” -> Chọn thư mục cần lưu -> Save', padx=30, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        filewin.mainloop()

    def ungdung(self):
        filewin = Toplevel()
        filewin.title("Ứng dụng")
        Label(filewin, fg="red", text="Ứng dụng:  NÂNG CAO CHẤT LƯỢNG ẢNH SỬ DỤNG THƯ VIỆN OPENCV", height="1",
              font=("Helvetica", 17), padx=100).pack()
        Label(filewin, text="Môn học: Nhập môn xử lý ảnh", height="1", font=("Helvetica", 17)).pack()
        Label(filewin, anchor="w", text="- Phiên bản: 1.0.0", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text="- Các thư viện hỗ trợ được sử dụng trong phần mềm:", height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ OpenCV', padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Tkinter', padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Numpy', padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Matplotlib', padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Scipy', padx=50, height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text="- Phần mềm được viết bằng Python 3.x", height="1",
              font=("Helvetica", 14)).pack(fill=X)

    def nhomthuchien(self):
        filewin = Toplevel()
        filewin.title("Nhóm thực hiện")
        Label(filewin, fg="red", text="NHÓM THỰC HIỆN", height="1", font=("Helvetica", 20), padx=200).pack()
        self.canvas = Canvas(filewin, width=200, height=200)

        Label(filewin, fg="blue", text="NHÓM 5", height="1", font=("Helvetica", 17), padx=200).pack()
        Label(filewin, anchor="w", text="- Thành viên thực hiện:", height="1", font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Nguyễn Văn An            20220185', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Nguyễn Ngọc Tú           20220135', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)
        Label(filewin, anchor="w", text='+ Vũ Thị Hồng Nhung        20220050', padx=50, height="1",
              font=("Helvetica", 14)).pack(fill=X)


def main():
    root = Tk()
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()      