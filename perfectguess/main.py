import random
n= random.randint(1, 100)
a=-1
guesses=0
while a != n:
    a=int(input("Guess the number:"))
    if a < n:
        print("Too low! Higher number please")
        guesses += 1
    elif a > n:
        print("Too high! Lower number please")
        guesses += 1
    else:
        print(f"Congratulations! You've guessed the number {n} in {guesses} attempts.")