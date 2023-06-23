from tkinter import *


class Labels(Label):
    def __init__(self, master, text):
        Label.__init__(self, master, relief=RAISED, font=('Arial', 20), width=25, border=5)
        self.color = 'grey60'
        self.hoverColor = 'grey40'
        self.selectedColor = 'grey50'
        self['bg'] = self.color
        self.rainbow_color = '0000FE'
        self['fg'] = f"#{self.rainbow_color}"
        self.text = text
        self['text'] = self.text
        self.bind("<Button-1>", self.clicked)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.victory = True
        self.val = 1

    def rainbow(self):
        self.rainbow_color = format(int(self.rainbow_color, 16) + self.val, 'X')
        if self.rainbow_color == 'FF':
            self.val = 256
        elif self.rainbow_color == 'FFFF':
            self.val = -1
        elif self.rainbow_color == 'FF00':
            self.val = 65536
        elif self.rainbow_color == 'FFFF00':
            self.val = -256
        elif self.rainbow_color == 'FF0000':
            self.val = 1
        elif self.rainbow_color == 'FF00FF':
            self.val = -65536

        if len(self.rainbow_color) < 6:
            self.rainbow_color = list(self.rainbow_color)
            for i in range(6 - len(self.rainbow_color)):
                self.rainbow_color.insert(0, '0')
            self.rainbow_color = "".join(self.rainbow_color)

        self['fg'] = f"#{self.rainbow_color}"

    def clicked(self, event):
        if self.victory:
            self['text'] = "What else do you want? 😑"
            self.victory = False
        else:
            self['text'] = self.text
            self.victory = True

    def enter(self, event):
        self['bg'] = self.hoverColor

    def leave(self, event):
        self['bg'] = self.color


class VictoryMenuFrame(Frame):
    def __init__(self, master, time):
        Frame.__init__(self, master)
        self.grid()

        self.time = time

        self.closeLabel = Label(text=' Close ', font=('Arial', 14), relief=RAISED, border=5, width=8)
        self.closeLabel.grid(row=2, column=0)
        self.closeLabel.bind("<Button-1>", self.closeClicked)
        self.closeLabel.bind("<Enter>", lambda event: self.enterButton(self.closeLabel))
        self.closeLabel.bind("<Leave>", lambda event: self.leaveButton(self.closeLabel))
        self.closeLabel['bg'] = 'grey60'

        self.victoryLabel = Labels(self, "Congratulations!\n You have completed the Maze!")
        self.victoryLabel.grid(row=1,column=0)

    def rainbow(self):
        self.victoryLabel.rainbow()
        self.master.after(self.time, self.rainbow)

    def closeClicked(self, event):
        # Closes the tkinter window so that the pygame window can continue functioning
        self.master.destroy()

    def enterButton(self, button):
        button['bg'] = 'grey40'

    def leaveButton(self, button):
        button['bg'] = 'grey60'


def victoryMenu(time=1):
    root = Tk()
    root.title('Victory')
    root.attributes('-topmost', True)
    menuFrame = VictoryMenuFrame(root, time)
    root['bg'] = 'grey20'
    root.after(time, menuFrame.rainbow)
    root.mainloop()


# Only runs this code if this is the main program being run (meaning this won't be run if it gets imported)
if __name__ == '__main__':
    victoryMenu(1)
