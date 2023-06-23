from tkinter import *


class Labels(Label):
    def __init__(self, master, colorType):
        Label.__init__(self, master, relief=RAISED, font=('Arial', 20), width=11, border=5)
        self.color = 'grey60'
        self.hoverColor = 'grey40'
        self.selectedColor = 'grey50'
        self.colorType = colorType
        self['bg'] = self.color
        self['text'] = f"Color Type - {self.colorType}"
        self.bind("<Button-1>", self.clicked)
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)
        self.selected = False
        if self.colorType == self.master.colorType:
            self.selected = True
            self['relief'] = SUNKEN
            self['bg'] = self.selectedColor

    def clicked(self, event):
        if not self.selected:
            self.selected = True
            self['bg'] = self.selectedColor
            self['relief'] = SUNKEN
            self.master.colorType = self.colorType
            for labelNum in self.master.colorLabels:
                if labelNum != self.colorType - 1:
                    self.master.colorLabels[labelNum].selected = False
                    self.master.colorLabels[labelNum]['bg'] = self.color
                    self.master.colorLabels[labelNum]['relief'] = RAISED

    def enter(self, event):
        if not self.selected:
            self['bg'] = self.hoverColor

    def leave(self, event):
        if not self.selected:
            self['bg'] = self.color

class PointMenuFrame(Frame):
    def __init__(self, master, colorType):
        Frame.__init__(self, master)
        self.grid()

        self.closeLabel = Label(text=' Close ', font=('Arial', 20), relief=RAISED, border=5, width=8)
        self.closeLabel.grid(row=0, column=0)
        self.closeLabel.bind("<Button-1>", self.closeClicked)
        self.closeLabel.bind("<Enter>", lambda event: self.enterButton(self.closeLabel))
        self.closeLabel.bind("<Leave>", lambda event: self.leaveButton(self.closeLabel))
        self.closeLabel['bg'] = 'grey60'

        self.startPath = Label(text='To Start', font=('Arial', 20), relief=RAISED, border=5, width=9)
        self.startPath.grid(row=1, column=0)
        self.startPath.bind("<Button-1>", self.pathToStartClicked)
        self.startPath.bind("<Enter>", lambda event: self.enterButton(self.startPath))
        self.startPath.bind("<Leave>", lambda event: self.leaveButton(self.startPath))
        self.startPath['bg'] = 'grey60'

    def closeClicked(self, event):
        # Closes the tkinter window so that the pygame window can continue functioning
        self.master.destroy()

    def pathToStartClicked(self, event):
        pass

    def enterButton(self, button):
        button['bg'] = 'grey40'

    def leaveButton(self, button):
        button['bg'] = 'grey60'


class PauseMenuFrame(Frame):
    def __init__(self, master, colorType):
        Frame.__init__(self, master)
        self.grid()

        self.colorLabel = Label(text='Color Type', font=('Arial', 20), relief=RAISED, border=5, width=9)
        self.colorLabel.grid(row=0, column=0)
        self.colorLabel.bind("<Button-1>", self.colorClicked)
        self.colorLabel.bind("<Enter>", lambda event: self.enterButton(self.colorLabel))
        self.colorLabel.bind("<Leave>", lambda event: self.leaveButton(self.colorLabel))
        self.colorLabel['bg'] = 'grey60'

        self.pauseLabel = Label(text=' UnPause ', font=('Arial', 20), relief=RAISED, border=5, width=8)
        self.pauseLabel.grid(row=1, column=0)
        self.pauseLabel.bind("<Button-1>", self.unpauseClicked)
        self.pauseLabel.bind("<Enter>", lambda event: self.enterButton(self.pauseLabel))
        self.pauseLabel.bind("<Leave>", lambda event: self.leaveButton(self.pauseLabel))
        self.pauseLabel['bg'] = 'grey60'

        self.colorBackLabel = Label(text='🢠Back', font=('Arial', 20), relief=RAISED, border=5)
        self.colorBackLabel.bind("<Button-1>", self.backClicked)
        self.colorBackLabel.bind("<Enter>", lambda event: self.enterButton(self.colorBackLabel))
        self.colorBackLabel.bind("<Leave>", lambda event: self.leaveButton(self.colorBackLabel))
        self.colorBackLabel['bg'] = 'grey60'

        self.colorType = colorType
        self.colorLabels = {}
        for labelNum in range(2):
            self.colorLabels[labelNum] = Labels(self, labelNum + 1)

    def unpauseClicked(self, event):
        # Closes the tkinter window so that the pygame window can continue functioning
        self.master.destroy()

    def colorClicked(self, event):
        self.grid()
        self.pauseLabel.grid_remove()
        self.colorLabel.grid_remove()
        for labelNum in self.colorLabels:
            self.colorLabels[labelNum].grid(column=0, row=labelNum)
        self.colorBackLabel.grid(column=0, row=3)

    def backClicked(self, event):
        for labelNum in self.colorLabels:
            self.colorLabels[labelNum].grid_remove()
        self.colorBackLabel.grid_remove()
        self.grid_remove()
        self.pauseLabel.grid(row=1, column=0)
        self.colorLabel.grid(row=0, column=0)
        self.master['bg'] = 'grey20'

    def enterButton(self, button):
        button['bg'] = 'grey40'

    def leaveButton(self, button):
        button['bg'] = 'grey60'


def pauseMenu(colorType):
    root = Tk()
    root.title('Pause Menu')
    menuFrame = PauseMenuFrame(root, colorType + 1)
    root['bg'] = 'grey20'
    root.mainloop()
    return menuFrame.colorType - 1


# Only runs this code if this is the main program being run (meaning this won't be run if it gets imported)
if __name__ == '__main__':
    difficulty = pauseMenu(1)
    print(f"The color type is '{difficulty}'")
