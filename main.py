from tkinter import Tk, Frame, Canvas, Label, Button, FLAT, DISABLED, NORMAL, PhotoImage
from random import randint

BACKGROUND_COLOR = "#F6FDC3"
LINE_COLOR = "#FF8080"
X_COLOR = "#FFCF96"
O_COLOR = "#CDFADB"

LARGE_FONT = ("Consolas", 35)
SMALL_FONT = ("Consolas", 20)

WINNER_CHECKS = {"column1": [0, 1, 2],
                 "column2": [3, 4, 5],
                 "column3": [6, 7, 8],
                 "row1": [0, 3, 6],
                 "row2": [1, 4, 7],
                 "row3": [2, 5, 8],
                 "diagonal1": [0, 4, 8],
                 "diagonal2": [2, 4, 6]}


def is_winner():
    buttons = [button for button in app.frames[GamePage].winfo_children() if isinstance(button, TicButton)]
    for check in WINNER_CHECKS.values():
        if buttons[check[0]]['text'] == buttons[check[1]]['text'] == buttons[check[2]]['text'] != "":
            for button in buttons:
                if button['state'] != DISABLED:
                    button['state'] = DISABLED
            app.after(800, lambda: app.end_game(player))
            return True
    moves_available = False
    for button in buttons:
        if button['state'] != DISABLED:
            moves_available = True
            break
    if not moves_available:
        app.after(800, lambda: app.end_game(None))
        return True
    else:
        return False


def change_player():
    if not is_winner():
        global player
        if player == player1:
            player = player2
        else:
            player = player1
        if not player.human:
            computer_play()


def computer_play():
    def check_signs_for(player):
        signs_in_row = 0
        row = None
        for check in WINNER_CHECKS.values():
            if not (buttons[check[0]]['state'] == buttons[check[1]]['state'] == buttons[check[2]]['state'] == DISABLED):
                for num in check:
                    if buttons[num]['text'] == player:
                        signs_in_row += 1
                        if signs_in_row > 1:
                            row = check
                            break
                signs_in_row = 0
        if row is not None:
            for num in row:
                if buttons[num]['state'] != DISABLED:
                    click_button(buttons[num])
                    return True
        return False

    def click_button(button: TicButton):
        button.after(300, lambda: button.on_click(None))

    buttons = [button for button in app.frames[GamePage].winfo_children() if isinstance(button, TicButton)]

    current_player = player.symbol
    player_to_check = player2.symbol
    if current_player == player2.symbol:
        player_to_check = player1.symbol

    # check if computer already has 2 signs in row and complete the row
    if not check_signs_for(current_player):
        # check if opponent has 2 signs in a row and block the row
        if not check_signs_for(player_to_check):
            if buttons[4]['state'] != DISABLED:
                click_button(buttons[4])
            else:
                random = randint(0, 8)
                while buttons[random]['state'] == DISABLED:
                    random = randint(0, 8)
                click_button(buttons[random])


class Player:
    def __init__(self, symbol: str = None, color: str = None, human: bool = True, font=("Arial", 150)):
        self.symbol = symbol
        self.color = color
        self.human = human
        self.font = font


class TicButton(Button):
    def __init__(self, master=None, h=300, w=300, **kwargs):
        super(TicButton, self).__init__(master=master, **kwargs)
        self.player = 0
        self.pixel = PhotoImage(width=1, height=1)
        self.config(
            relief=FLAT,
            bd=0,
            highlightthickness=0,
            image=self.pixel,
            height=int(h/3) - 15,
            width=int(w/3) - 15,
            compound="top",
            padx=0,
            pady=0,
            background=master['background'],
            activebackground=master['background'],
        )

        # Bind events
        self.bind("<ButtonRelease>", self.on_click)

    def on_click(self, event):
        if self['state'] != DISABLED:
            self.player = player
            self.config(font=player.font,
                        text=player.symbol,
                        state=DISABLED,
                        disabledforeground=player.color)
            change_player()


class TkinterApp(Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, GamePage, EndPage):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.start_page()

    def start_page(self):
        for button in self.frames[GamePage].winfo_children():
            if isinstance(button, TicButton):
                if button['state'] == DISABLED:
                    button.config(
                        state=NORMAL,
                        text=""
                    )
        self.frames[StartPage].hide_player_choice()
        global player
        player = player2
        frame = self.frames[StartPage]
        frame.tkraise()

    # to display the current frame passed as parameter
    def game_page(self, human1: bool = True, human2: bool = True):
        player1.human = human1
        player2.human = human2
        change_player()
        frame = self.frames[GamePage]
        frame.tkraise()

    def end_game(self, winner):
        frame = self.frames[EndPage]
        if winner is not None:
            frame.label.config(
                text=f"The winner is"
            )
            frame.winner.config(font=player.font,
                                text=player.symbol,
                                state=DISABLED,
                                disabledforeground=player.color,)
        else:
            frame.label.config(
                text=f"Draw"
            )
            frame.winner.config(font=player.font,
                                text="",
                                state=DISABLED,
                                disabledforeground=player.color,)
        frame.tkraise()


# first window frame startpage
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.config(self, background=BACKGROUND_COLOR, height=500, width=500)

        label = Label(self, text="Tic Tac Toe", font=LARGE_FONT, background=BACKGROUND_COLOR, foreground=LINE_COLOR,
                      width=19)
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        button_2players = Button(self, text="2 players",
                                 command=lambda human1=True, human2=True: controller.game_page(human1, human2))
        button_2players.config(
            font=SMALL_FONT,
            relief=FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            foreground=LINE_COLOR,
            background=X_COLOR,
            activebackground=O_COLOR,
            activeforeground=LINE_COLOR,
        )
        button_2players.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.button_computer = Button(self, text="Against computer", command=self.switch_player_choice)
        self.button_computer.config(
            font=SMALL_FONT,
            relief=FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            foreground=LINE_COLOR,
            background=X_COLOR,
            activebackground=O_COLOR,
            activeforeground=LINE_COLOR,
        )
        self.button_computer.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        pixel = PhotoImage(width=1, height=1)
        self.label_player1 = Label(self, text="Player 1", font=SMALL_FONT, background=BACKGROUND_COLOR,
                                   foreground=LINE_COLOR)
        self.button_player1 = Button(self,
                                     relief=FLAT,
                                     bd=0,
                                     highlightthickness=0,
                                     font=player1.font,
                                     text=player1.symbol,
                                     image=pixel,
                                     height=100,
                                     width=100,
                                     compound="top",
                                     foreground=player1.color,
                                     background=BACKGROUND_COLOR)
        self.button_player1.bind("<ButtonRelease>",
                                 lambda human1=True, human2=False: controller.game_page(human1=True, human2=human2))
        self.label_player2 = Label(self, text="Player 2", font=SMALL_FONT, background=BACKGROUND_COLOR,
                                   foreground=LINE_COLOR)
        self.button_player2 = Button(self,
                                     relief=FLAT,
                                     bd=0,
                                     highlightthickness=0,
                                     font=player2.font,
                                     text=player2.symbol,
                                     image=pixel,
                                     height=100,
                                     width=100,
                                     compound="top",
                                     foreground=player2.color,
                                     background=BACKGROUND_COLOR)
        self.button_player2.bind("<ButtonRelease>",
                                 lambda human1=False, human2=True: controller.game_page(human1=False, human2=human2))

    def switch_player_choice(self):
        if self.label_player1.winfo_ismapped():
            self.hide_player_choice()
        else:
            self.show_player_choice()

    def show_player_choice(self):
        self.button_computer.config(background=O_COLOR)
        self.label_player1.grid(row=3, column=0, padx=10, pady=0)
        self.label_player2.grid(row=3, column=1, padx=10, pady=0)
        self.button_player1.grid(row=4, column=0, padx=10, pady=0)
        self.button_player2.grid(row=4, column=1, padx=10, pady=0)

    def hide_player_choice(self):
        self.button_computer.config(background=X_COLOR)
        self.label_player1.grid_forget()
        self.label_player2.grid_forget()
        self.button_player1.grid_forget()
        self.button_player2.grid_forget()


# second window frame page1
class GamePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background=BACKGROUND_COLOR)
        self.c = Canvas(self, height=500, width=500, highlightthickness=0, bg=BACKGROUND_COLOR)
        self.c.grid(row=0, column=0, columnspan=3, rowspan=3)
        self.c.bind('<Configure>', self.create_grid)

    def create_grid(self, event=None):
        w = self.c.winfo_width()  # Get current width of canvas
        h = self.c.winfo_height()  # Get current height of canvas

        # Creates two vertical lines
        self.c.create_line([(w / 3, 0), (w / 3, h)], smooth=True, width=10, fill=LINE_COLOR)
        self.c.create_line([(w / 3 * 2, 0), (w / 3 * 2, h)], smooth=True, width=10, fill=LINE_COLOR)

        # Creates all horizontal lines at intervals of 100
        self.c.create_line([(0, h / 3), (w, h / 3)], smooth=True, width=10, fill=LINE_COLOR)
        self.c.create_line([(0, h / 3 * 2), (w, h / 3 * 2)], smooth=True, width=10, fill=LINE_COLOR)

        for i in range(0, 3):
            for x in range(0, 3):
                button = TicButton(self, w, h)
                button.grid(row=i, column=x, padx=5, pady=5)


# third window frame page2
class EndPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background=BACKGROUND_COLOR)
        self.label = Label(self, text="Page 2", font=LARGE_FONT, foreground=LINE_COLOR, background=BACKGROUND_COLOR,
                           width=19)
        self.label.grid(row=0, padx=10, pady=10)

        self.winner = TicButton(self)
        self.winner.config(state=DISABLED, height=100, width=100)
        self.winner.grid(row=1, padx=20, pady=50)

        button_new_game = Button(self, text="New game", command=lambda player="human": controller.start_page())
        button_new_game.config(
            font=SMALL_FONT,
            relief=FLAT,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10,
            foreground=LINE_COLOR,
            background=X_COLOR,
            activebackground=O_COLOR,
            activeforeground=LINE_COLOR,
        )
        button_new_game.grid(row=2, padx=10, pady=10)


player1 = Player(symbol="×", color=X_COLOR, human=True, font=("Arial", 150))
player2 = Player(symbol="ⵔ", color=O_COLOR, human=True, font=("Arial", 90, "bold"))

player = player2

# Driver Code
app = TkinterApp()
app.title("Tic Tac Toe")
app.config(padx=50, pady=50, background=BACKGROUND_COLOR)
app.resizable(False, False)
app.mainloop()
