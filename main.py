import pygame
import random

pygame.init()

# the display
win = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Hangman")

# each letter of the alphabet will be an object of this class
class Letter:
    # initialising the object
    def __init__(self, character, x, y):
        self.character = character
        self.x = x
        self.y = y
        self.guessed = False
        self.font = pygame.font.SysFont("freesansbold", 30)
        self.text = self.font.render(self.character, 1, (0, 0, 0))

    # displaying the letter
    def drawSelf(self, game_word):
        # if it is a letter that has been correctly guessed display it with a green background
        if self.guessed and self.character in game_word:
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(self.x - 4, self.y - 2, 30, 30))
        # if it is a letter that has been incorrectly guessed display it with a red background
        elif self.guessed:
            pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x - 4, self.y - 2, 30, 30))
        # if it is a letter that has not been guessed display it with a grey background
        else:
            pygame.draw.rect(win, (211, 211, 211), pygame.Rect(self.x - 4, self.y - 2, 30, 30))
        # displaying the letter itself
        win.blit(self.text, (self.x, self.y))

    # displaying the letter in the appropriate position(s) if it has been guessed and is correct
    def checkCorrectGuess(self, x, y):
        if self.guessed:
            font = pygame.font.SysFont("freesansbold", 30)
            text = font.render(self.character, 1, (0, 0, 0))
            width, height = font.size(self.character)
            x_change = (20 - width) / 2
            win.blit(text, (x + int(x_change), y - 20))

# creating the wordlist and randomly selecting a word from it
def generateWord():
    word_file = open("word_list.txt", "r")
    word_list = []
    for line in word_file:
        word_list.append(line.strip())
    word_file.close()
    random_word = word_list[random.randint(0, len(word_list) - 1)]
    return random_word

# counting the number of wrong guesses the player has made
def countWrong(letter_list, game_word):
    counter = 0
    for current_letter in letter_list:
        if current_letter.character not in game_word and current_letter.guessed:
            counter += 1
    return counter

# displaying the hangman
def displayHangman(wrong_guesses):
    # displaying the gallows
    pygame.draw.line(win, (0, 0, 0), (100, 350), (200, 350), 10)
    pygame.draw.line(win, (0, 0, 0), (150, 350), (150, 100), 10)
    pygame.draw.line(win, (0, 0, 0), (146, 100), (250, 100), 10)
    pygame.draw.line(win, (0, 0, 0), (245, 100), (245, 130), 10)

    if wrong_guesses >= 1:
        # draw head
        pygame.draw.circle(win, (0, 0, 0), [245, 155], 25, 10)
        if wrong_guesses >= 2:
            # draw body
            pygame.draw.line(win, (0, 0, 0), (245, 175), (245, 250), 10)
            if wrong_guesses >= 3:
                # draw left arm
                pygame.draw.line(win, (0, 0, 0), (245, 190), (210, 225), 10)
                if wrong_guesses >= 4:
                    # draw right arm
                    pygame.draw.line(win, (0, 0, 0), (245, 190), (280, 225), 10)
                    if wrong_guesses >= 5:
                        # draw left leg
                        pygame.draw.line(win, (0, 0, 0), (245, 250), (210, 285), 10)
                        if wrong_guesses >= 6:
                            # draw right leg
                            pygame.draw.line(win, (0, 0, 0), (245, 250), (280, 285), 10)

# checking if the player has won/lost
def checkWin(wrong_guesses, letter_list, game_word, alphabet_list):
    # if they have made 6 wrong guesses then they have lost
    if wrong_guesses >= 6:
        return "Lost"
    else:
        counter = 0
        # checking if they have guessed every letter in the word
        for i in range(len(game_word)):
            if letter_list[alphabet_list.index(game_word[i])].guessed:
                counter += 1
        # if they have guessed every letter in the word they have won
        if counter == len(game_word):
            return "Won"
        else:
            return "Neither"

# updating the display appropriately
def drawWindow(letter_list, game_word, alphabet_list, game_over, key_pressed=-1):
    # giving the window a background colour of white
    win.fill((255, 255, 255))

    # if the player has pressed an alphabet key, set the letter to guessed
    if key_pressed >= 0 and not game_over:
        letter_list[key_pressed].guessed = True

    # display each letter at the bottom showing correct/incorrect guesses
    for letter in letter_list:
        letter.drawSelf(game_word)

    # the starting x and y positions for the dashed lines representing the word
    x = 400
    y = 300

    # drawing the dashed lines representing the word
    for i in range(len(game_word)):
        pygame.draw.line(win, (0, 0, 0), (x, y), (x + 20, y), 4)
        letter_list[alphabet_list.index(game_word[i])].checkCorrectGuess(x, y)
        x += 25

    # displaying the hangman based on the amount of incorrect guesses
    displayHangman(countWrong(letter_list, game_word))

    # checking if the game has been won
    win_state = checkWin(countWrong(letter_list, game_word), letter_list, game_word, alphabet_list)

    # if the game has been won or lost display the replay button with the appropriate win/lose message
    if win_state != "Neither":
        pygame.draw.rect(win, (0, 0, 0), pygame.Rect(300, 200, 200, 100))

        if win_state == "Won":
            to_display = "You win :)"
        else:
            to_display = "The answer was: " + game_word
            font = pygame.font.SysFont("Free Sans Bold", 15)
            text = font.render(to_display, 1, (255, 255, 255))
            word_length, word_height = font.size(to_display)
            x_change = int((200 - word_length) / 2)
            y_change = int((100 - word_height) / 2)
            win.blit(text, (300 + x_change, 200 + y_change + 15))
            to_display = "You lose :("

        font = pygame.font.SysFont("Free Sans Bold", 30)
        text = font.render(to_display, 1, (255, 255, 255))
        word_length, word_height = font.size(to_display)
        x_change = int((200 - word_length) / 2)
        y_change = int((100 - word_height) / 2)
        win.blit(text, (300 + x_change, 200 + y_change - 10))

        to_display = "Click this button to replay"
        font = pygame.font.SysFont("Free Sans Bold", 15)
        text = font.render(to_display, 1, (255, 255, 255))
        word_length, word_height = font.size(to_display)
        x_change = int((200 - word_length) / 2)
        win.blit(text, (300 + x_change, 200 + y_change + 40))
        return True
    else:
        return False

# generating the list of letter objects and their positions at the bottom of the screen
def generateLetterList(alphabet_list):
    x = 210
    y = 430
    letter_list = []
    for i in range(26):
        letter_list.append(Letter(alphabet_list[i], x, y))
        x += 30
        if i == 12:
            x = 210
            y += 30
    return letter_list

# initialising variables
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
word = generateWord()
letters = generateLetterList(alphabet)

# main loop
run = True
gameOver = False
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        # handling the user pressing a key
        if event.type == pygame.KEYDOWN:
            keyPressed = event.unicode
            try:
                # updating the display to reflect any changes as a result of the key press
                gameOver = drawWindow(letters, word, alphabet, gameOver, alphabet.index(keyPressed))
                pygame.display.update()
            # deals with the user pressing a non-alphabetic key
            except ValueError as error:
                pass

        # checking if the user has clicked the replay button and restarting the game if they have
        if event.type == pygame.MOUSEBUTTONDOWN and gameOver:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 300 <= mouse_x <= 500 and 200 <= mouse_y <= 300:
                word = generateWord()
                letters = generateLetterList(alphabet)
                gameOver = False

    # always updating the display
    drawWindow(letters, word, alphabet, gameOver)
    pygame.display.update()
