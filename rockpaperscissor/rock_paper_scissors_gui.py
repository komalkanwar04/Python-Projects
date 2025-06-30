import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.configure(bg="#f0f0e0")
        self.user_score = 0
        self.computer_score = 0

        self.choices = ['rock', 'paper', 'scissors']

        self.create_widgets()
        self.update_score()

    def create_widgets(self):
        self.label_instruction = tk.Label(self.root, text="Please select Rock, Paper, or Scissors to play the game:", font=("Arial", 14))
        self.label_instruction.pack(pady=10)

        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(pady=5)

        self.btn_rock = tk.Button(self.frame_buttons, text="Rock", width=10, bg="orange", command=lambda: self.play('rock'))
        self.btn_rock.grid(row=0, column=0, padx=5)

        self.btn_paper = tk.Button(self.frame_buttons, text="Paper", width=10, bg="blue", fg="white", command=lambda: self.play('paper'))
        self.btn_paper.grid(row=0, column=1, padx=5)

        self.btn_scissors = tk.Button(self.frame_buttons, text="Scissors", width=10, bg="green", fg="white", command=lambda: self.play('scissors'))
        self.btn_scissors.grid(row=0, column=2, padx=5)

        self.label_result = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_result.pack(pady=10)

        self.label_score = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_score.pack(pady=10)

        self.btn_reset = tk.Button(self.root, text="Reset Game", bg="red", fg="white", command=self.reset_game)
        self.btn_reset.pack(pady=10)

    def play(self, user_choice):
        computer_choice = random.choice(self.choices)
        winner = self.determine_winner(user_choice, computer_choice)
        self.display_result(user_choice, computer_choice, winner)
        self.update_score()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'scissors' and computer_choice == 'paper') or \
             (user_choice == 'paper' and computer_choice == 'rock'):
            self.user_score += 1
            return "user"
        else:
            self.computer_score += 1
            return "computer"

    def display_result(self, user_choice, computer_choice, winner):
        result_text = f"You chose: {user_choice}\nComputer chose: {computer_choice}\n"
        if winner == "tie":
            result_text += "It's a tie!"
        elif winner == "user":
            result_text += "You win!"
        else:
            result_text += "You lose!"
        self.label_result.config(text=result_text)

    def update_score(self):
        score_text = f"Score - You: {self.user_score} | Computer: {self.computer_score}"
        self.label_score.config(text=score_text)

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.label_result.config(text="")
        self.update_score()

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
