# Load words and remove anything not 5 characters long
invalid_letters = []
valid_letters = {} #letter and position
wordlist = []
result = ''
word_length = int(input("How many letters:")) # how long are the words we're guessing?

print("\n\nWORDLE ASSIST")
print("For inputs, use the following key per letter\t! = exact, ? = close, X = none")

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def list_dedupe(oglist):
    # input list, output deduplicated list
    newlist = []
    for item in oglist:
        if item not in newlist:
            newlist.append(item)
    return newlist

def get_input(word_length=word_length):        
    # Get user input
    guess = input("\tGuess=").lower()
    result = input("\tResult '!?x'=").lower()
    if len(guess) == len(result) and len(guess) == word_length:
        return guess,result
    else:
        guess,result = get_input()
        return guess,result

def filter_wordlist(wordlist,result,guess,valid_letters,invalid_letters):
    # Iterate and remove words that don't fit the results
    remove_words = [] #Words to remove
    
    for position in range(len(result)):
        guess_letter = guess[position]
        result_letter = result[position]
        
        if result_letter == "?" and result_letter not in valid_letters:
            valid_letters[guess_letter] = -1 # valid letter, but not this location
        elif result_letter == "!":
            valid_letters[guess_letter] = position

        if result_letter == "x":
            # Remove anything with this letter from results,
            #  unless it's been validated before which happens when there are more than 1 of the letter
            invalid_letters.append(guess_letter)

            for word in wordlist:
                if (guess_letter in word) and (guess_letter not in valid_letters):
                    remove_words.append(word)
                    
        elif result_letter == "?":
            # Remove anything that doesn't have at least one of these letters
            for word in wordlist:
                if guess_letter not in word:
                    remove_words.append(word)
                    
            # Remove any word with this letter in this exact position!
            for word in wordlist:
                if word[position] == guess_letter:
                    remove_words.append(word)

        elif result_letter == "!":
            # Remove anything that doesn't have a letter in this position
            for word in wordlist:
                if word[position] != guess_letter:
                    remove_words.append(word)
    
    # remove reults from wordlist        
    for word in remove_words:
        if word in wordlist:
            wordlist.remove(word)
            
    return wordlist, valid_letters, invalid_letters

def letter_frequency(wordlist):
    # identifies frequency of remaining words
    frequencystring = "".join(wordlist)
    frequency_dict = {}
    
    for i in frequencystring:
        if i in frequency_dict:
            frequency_dict[i] += 1
        else:
            frequency_dict[i] = 1
            
    return frequency_dict

def combine_dict(input_dict):
    # Combines the lists of input dictionary into a non-duplicated list
    output_list = []
    for key in input_dict.keys():
        for item in input_dict[key]:
            if item not in output_list:
                output_list.append(item)
    return output_list

def unique(original_wordlist,valid_letters,invalid_letters,original_freq):
    # Return word with highest score based on frequency and being not found...and unique letter
    max_score = 0
    rec_dictionary = {}    
    rec_dictionary['3'] = []
    rec_dictionary['2'] = []
    rec_dictionary['1'] = []

    for word in original_wordlist:
        score = 0
        reject = False
        for pos in range(len(word)):
            letter = word[pos]
            if word.count(letter) > 1: # ignore words with more than one of same letterar
                reject = True
            if letter in invalid_letters:
                reject = True
            elif letter in valid_letters:
                if valid_letters[letter] == pos: #In same spot
                    reject = True
                else: # valid letter but different spot
                    score = (score / 2)
            else:
                #score based on frequency
                score += original_freq[letter]

        # add to list if tie, start new list if higher
        if reject == True:
            pass # don't even consider the word
        elif score == max_score:
            rec_dictionary['1'].append(word)
        elif score > max_score:
            rec_dictionary['3'] = rec_dictionary['2']
            rec_dictionary['2'] = rec_dictionary['1']
            rec_dictionary['1'] = [word]
            max_score = score
    
    print("Best filters: ",combine_dict(rec_dictionary))

def recommend(wordlist,valid_letters):
    # recommend word from remaining wordlist by suggesting word with least known letters to maximize search
    freq = letter_frequency(wordlist)
    
    rec_dictionary = {}    
    rec_dictionary['3'] = []
    rec_dictionary['2'] = []
    rec_dictionary['1'] = []
 
    max_score = 0 #score of highest recommendation(s)
    
    #Score by frequency rank only, if valid letter, score for that letter is zero.
    for word in wordlist:
        score = 0
        for letter in word: #guaranteed to existsince frequency dist is based on this list
            if letter not in valid_letters and word.count(letter) == 1:
                score += freq[letter]
            if letter in valid_letters: #less weight if already found
                score += freq[letter] / 2
        
        # add to list if tie, start new list if higher
        if score == max_score:
            rec_dictionary['1'].append(word)
        elif score > max_score:
            rec_dictionary['3'] = rec_dictionary['2']
            rec_dictionary['2'] = rec_dictionary['1']
            rec_dictionary['1'] = [word]
            max_score = score

    wordlist = list_dedupe(wordlist) # remove duplicates, if any
    a_number = 1/len(wordlist)
    percentage = "{:.0%}".format(a_number)
    results = combine_dict(rec_dictionary)
    print("Best guesses:",results,"- Probability: ",percentage)


# Load in word list and filter to correct length
def loadwords():
    xwordlist = []
    for word in load_words():
        if len(word) == word_length:
            xwordlist.append(word)
    return xwordlist

wordlist = loadwords()
oglist = loadwords()
ogfreq = letter_frequency(oglist)

while result != '!' * word_length:
    print("\n")
    
    # Make a recommendation
    recommend(wordlist,valid_letters)
    unique(oglist,valid_letters,invalid_letters,ogfreq)

    # Gather input
    guess, result = get_input()
    
    # Get user input and filter list
    wordlist, valid_letters, invalid_letters = filter_wordlist(wordlist,result,guess,valid_letters,invalid_letters)

print('Solved!')
