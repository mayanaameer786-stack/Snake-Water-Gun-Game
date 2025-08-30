import tkinter as tk
import random

# Choices mapping
your_dict = {"s": 1, "g": 0, "w": -1}
reverse_dict = {1: "Snake", 0: "Gun", -1: "Water"}

# Global variables
your_score = 0
computer_score = 0
rounds = 0
current_round = 0
player_name = "You"
choice_made = False

timer_id = None

# Functions
def start_game():
    global rounds, your_score, computer_score, current_round, player_name

    try:
        rounds = int(rounds_entry.get())
        if rounds <= 0:
            result_label.config(text="⚠️ Enter positive rounds!")
            return
    except:
        result_label.config(text="⚠️ Enter a valid number!")
        return

    player_name = name_entry.get().strip() or "You"

    your_score = 0
    computer_score = 0
    current_round = 0
    result_label.config(text=f"Game Started! {player_name}, make your choice.")
    score_label.config(text=f"{player_name}: 0 | Computer: 0")
    enable_buttons()

    start_timer()


def start_timer():
    global timer_id, choice_made
    choice_made = False
    countdown(5)

def countdown(time_left):
    global timer_id, choice_made
    if choice_made:
        return
    if time_left <= 0:
        auto_lose()
        return
    timer_label.config(text=f"⏳ Time left: {time_left}s")
    timer_id = root.after(1000, countdown, time_left - 1)

def auto_lose():
    global computer_score, current_round
    computer_score += 1
    current_round += 1
    update_result("⌛ Time up! You missed this round. Computer scores!")


def play(choice):
    global your_score, computer_score, current_round, choice_made
    choice_made = True

    if timer_id:
        root.after_cancel(timer_id)

    if current_round >= rounds:
        result_label.config(text="Game Over! Restart to play again.")
        return

    computerchoice = random.choice([-1, 0, 1])
    you = your_dict[choice]

    current_round += 1

    round_info = f"Round {current_round}/{rounds}\n{player_name}: {reverse_dict[you]} | Computer: {reverse_dict[computerchoice]}\n"

    if computerchoice == you:
        result_text = round_info + "🤝 Tie!"
    elif (computerchoice == 1 and you == 0) or (computerchoice == 0 and you == -1) or (computerchoice == -1 and you == 1):
        your_score += 1
        result_text = round_info + f"🎉 {player_name} won this round!"
    else:
        computer_score += 1
        result_text = round_info + "💻 Computer won this round!"

    update_result(result_text)


def update_result(text):
    score_label.config(text=f"{player_name}: {your_score} | Computer: {computer_score}")

    if current_round == rounds:
        if your_score > computer_score:
            final = f"🏆 Congratulations {player_name}! You won the match."
        elif your_score < computer_score:
            final = "😢 You lost. Try again!"
        else:
            final = "🤝 Match Tie!"
        disable_buttons()
        result_label.config(text=text + "\n" + final)
    else:
        result_label.config(text=text)
        start_timer()


def replay_game():
    start_game()


def enable_buttons():
    snake_button.config(state="normal")
    gun_button.config(state="normal")
    water_button.config(state="normal")

def disable_buttons():
    snake_button.config(state="disabled")
    gun_button.config(state="disabled")
    water_button.config(state="disabled")

# Dark/Light Mode
def toggle_theme():
    if root["bg"] == "#f0f0f0":
        root.config(bg="#222")
        welcome_label.config(bg="#222", fg="white")
        score_label.config(bg="#222", fg="white")
        result_label.config(bg="#222", fg="white")
        timer_label.config(bg="#222", fg="white")
    else:
        root.config(bg="#f0f0f0")
        welcome_label.config(bg="#f0f0f0", fg="black")
        score_label.config(bg="#f0f0f0", fg="black")
        result_label.config(bg="#f0f0f0", fg="black")
        timer_label.config(bg="#f0f0f0", fg="black")


# GUI Setup
root = tk.Tk()
root.title("Snake Water Gun Game")
root.geometry("450x500")
root.config(bg="#f0f0f0")

# Widgets
welcome_label = tk.Label(root, text="🎮 Snake Water Gun Game", font=("Arial", 16, "bold"), bg="#f0f0f0")
welcome_label.pack(pady=10)

name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.pack(pady=5)
name_entry.insert(0, "Player1")

rounds_entry = tk.Entry(root, font=("Arial", 12))
rounds_entry.pack(pady=5)
rounds_entry.insert(0, "3")

start_button = tk.Button(root, text="Start Game", font=("Arial", 12, "bold"), command=start_game, bg="#4CAF50", fg="white")
start_button.pack(pady=5)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

snake_button = tk.Button(frame, text="🐍 Snake", font=("Arial", 12, "bold"), width=10, command=lambda: play("s"))
snake_button.grid(row=0, column=0, padx=5)

gun_button = tk.Button(frame, text="🔫 Gun", font=("Arial", 12, "bold"), width=10, command=lambda: play("g"))
gun_button.grid(row=0, column=1, padx=5)

water_button = tk.Button(frame, text="💧 Water", font=("Arial", 12, "bold"), width=10, command=lambda: play("w"))
water_button.grid(row=0, column=2, padx=5)

score_label = tk.Label(root, text="You: 0 | Computer: 0", font=("Arial", 12, "bold"), bg="#f0f0f0")
score_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f0f0f0", wraplength=400, justify="center")
result_label.pack(pady=10)

timer_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
timer_label.pack(pady=5)

replay_button = tk.Button(root, text="🔄 Replay", font=("Arial", 12, "bold"), command=replay_game, bg="#2196F3", fg="white")
replay_button.pack(pady=5)

theme_button = tk.Button(root, text="🌗 Toggle Theme", font=("Arial", 12, "bold"), command=toggle_theme)
theme_button.pack(pady=5)

root.mainloop()
