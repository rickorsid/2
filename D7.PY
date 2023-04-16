from tkinter import *
from PIL import ImageTk, Image
import random
import openpyxl
class Model:
    def __init__(self, file):
        self.workbook = openpyxl.load_workbook(file)
        self.worksheet = self.workbook.active
        self.questions = [row for row in self.worksheet.iter_rows(min_row=2, values_only=True)]
    def pick_question(self, question_type):
        questions = [q for q in self.questions if q[1] == question_type]
        if not questions:
            return None
        return random.choice(questions)
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_question = None
        self.question_type = '单选题'
        self.view.bind_choose_question_button(self.choose_question)
        self.view.bind_show_answer_button(self.show_answer)
        self.view.bind_change_question_type_buttons(self.change_question_type)
        self.time_elapsed = 0
        self.timer_id = None
    def start_timer(self):
        self.time_elapsed += 1
        self.view.update_timer(self.time_elapsed)
        self.timer_id = self.view.master.after(1000, self.start_timer)
    def stop_timer(self):
        if self.timer_id:
            self.view.master.after_cancel(self.timer_id)
    def start(self):
        self.view.run()
    def choose_question(self):
        self.stop_timer()
        self.time_elapsed = 0
        self.view.update_timer(self.time_elapsed)
        self.current_question = self.model.pick_question(self.question_type)
        if self.current_question:
            self.view.show_question(self.current_question)
            self.start_timer()
        else:
            self.view.show_message('没有该题型的题目')
    def show_answer(self):
        if self.current_question:
            self.view.show_answer(self.current_question[3])
    def change_question_type(self, question_type):
        self.question_type = question_type
        self.view.show_message(f'当前题型：{question_type}')
        self.choose_question()
class View:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True)
        # 设置背景图片
        self.background_image = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.background_label = Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # 设置题目、答案和按钮
        self.timer_label = Label(self.master, font=('微软雅黑', 24), background='#aa2116', fg='white')
        self.timer_label.pack(side=TOP, padx=10, pady=5)
        self.question_number_label = Label(self.master, font=('微软雅黑', 26),background='#aa2116',fg='white')
        self.question_number_label.pack(anchor='nw', padx=50, pady=1)
        self.question_type_label = Label(self.master, font=('微软雅黑', 26),background='#aa2116',fg='white',)
        self.question_type_label.pack(anchor='nw', padx=50, pady=1)
        self.question_label = Label(self.master,font=('微软雅黑', 30), wraplength=1800,justify='left',background='#aa2116',fg='white')
        self.question_label.pack(anchor='nw', padx=50, pady=1)
        self.answer_label = Label(self.master, font=('微软雅黑', 30), wraplength=1800, justify='left',background='#aa2116',fg='white')
        self.answer_label.pack(anchor='nw', padx=50, pady=20)
        self.button_frame = Frame(self.master,background='#aa2116')
        self.button_frame.pack(side=BOTTOM,anchor='nw',pady=1)
        self.change_question_type_buttons = {}
        for question_type in ['单选题', '多选题', '填空题', '判断题', '简答题10分', '简答题20分', '简答题30分']:
            button = Button(self.button_frame, text=question_type, font=('仿宋', 24),background='#aa2116')
            button.pack(side=LEFT, padx=10)
            self.change_question_type_buttons[question_type] = button
        self.choose_question_button = Button(self.master, text='抽题', font=('仿宋', 24),background='#aa2116')
        self.choose_question_button.pack(side=LEFT, anchor='se', padx=10, pady=10)
        self.show_answer_button = Button(self.master, text='显示答案', font=('仿宋', 24),background='#aa2116')
        self.show_answer_button.pack(side=LEFT, anchor='se', padx=10, pady=10)
        self.close_button = Button(self.master, text='关闭', font=('仿宋', 24),background='#aa2116', command=self.master.destroy)
        self.close_button.pack(side=RIGHT, anchor='se', padx=10, pady=10)
        # 设置 type_label
        self.type_label = Label(self.master, text='当前题型：单选题', font=('仿宋', 24),background='#aa2116')
        self.type_label.pack(side=BOTTOM, fill=X, padx=10, pady=10)
    def run(self):
        self.master.mainloop()
    def bind_choose_question_button(self, callback):
        self.choose_question_button.config(command=callback)
    def bind_show_answer_button(self, callback):
        self.show_answer_button.config(command=callback)
    def bind_change_question_type_buttons(self, callback):
        for question_type, button in self.change_question_type_buttons.items():
            button.config(command=lambda question_type=question_type: callback(question_type))
    def show_question(self, question):
        question_number, question_type, question_content, answer = question
        self.question_number_label.config(text=f'题目：第  {question_number}  题')
        self.question_type_label.config(text=f'{question_type}')
        if question_type == '判断题':
            self.question_label.config(text=f'{question_content}', font=('微软雅黑', 22))
        else:
            self.question_label.config(text=f'{question_content}', font=('微软雅黑', 36))
        self.answer_label.config(text='')
        self.question_label.config(text=f'{question_content}')
        self.answer_label.config(text='')
    def show_answer(self, answer):
        self.answer_label.config(text=f' 答案：{answer}')
    def show_message(self, message):
        self.question_number_label.config(text='')
        self.question_type_label.config(text='')
        self.question_label.config(text='')
        self.answer_label.config(text='')
        self.type_label.config(text=message)
    def update_timer(self, time):
        self.timer_label.config(text=f'用时：{time}s')
# 创建 MVC 实例
model = Model('questions.xlsx')
root = Tk()
root.title("题库")
view = View(root)
controller = Controller(model, view)
controller.start()