from sqlite3 import Row
from selenium import webdriver
from pyshadow.main import Shadow
from selenium.webdriver.common.keys import Keys
from time import sleep
import random

# selenium stuff
url = 'https://www.powerlanguage.co.uk/wordle/'
browser = webdriver.Firefox()
shadow = Shadow(browser)
type(browser)
browser.get(url)

# opens list of 5 letter words from file
with open('words.txt') as f:
    word_list = f.read().splitlines()

guess = ''

def guessing():
    global guess
    present = []
    buttons = shadow.find_elements('div.row button')
    for l in buttons:
        letter = l.text.lower()
        # if letter is in correct position
        if l.get_attribute('data-state') == 'correct':
            present.append(letter)
            position = guess.find(letter)
            # remove all words that do not have that letter in the correct position from word list
            for word in word_list[:]:
                if letter not in word[position]:
                    print('%s does not contain %s in position %s, removing' % (word, letter, position))
                    word_list.remove(word)                    
        elif l.get_attribute('data-state') == 'present':
            present.append(letter)
            position = guess.find(letter)
            # remove all words without letter from word list
            for word in word_list[:]:
                if letter not in word:
                    print('%s does not contain %s, removing' % (word, letter))
                    word_list.remove(word)
            # remove all words with letter in position from word list
            for word in word_list[:]:
                if letter in word[position]:
                    print('%s contains %s in position %s, removing' % (word, letter, position))
                    word_list.remove(word)
        elif l.get_attribute('data-state') == 'absent':
            for word in word_list[:]:
                if letter in word and letter not in present:
                    print('%s contains %s, removing' % (word, letter))
                    word_list.remove(word)          
    # create new guess with updated list
    guess = word_list[random.randint(0,len(word_list)-1)]
    print('Guess: %s' % guess)
    print('Possible guesses remaining: %s' % len(word_list))

# closes tutorial
body = browser.find_element_by_xpath('/html/body')
body.click()

while True:
    guessing()
    body.send_keys(guess)
    body.send_keys(Keys.RETURN)
    for game_row in shadow.find_elements('game-row'):
        if game_row.get_attribute('letters') == guess:
            if game_row.get_attribute('invalid') == "":
                print('%s is not in word list' % guess)
                word_list.remove(guess)
                for x in range (0, 5):
                    body.send_keys(Keys.BACKSPACE)
    sleep(3)