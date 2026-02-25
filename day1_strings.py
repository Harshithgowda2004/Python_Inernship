# Remove vowels from a string
# If vowels occur together, all are removed

def remove_vowels(s):
    vowels = "aeiouAEIOU"
    result = ""

    for ch in s:
        if ch not in vowels:
            result += ch

    return result


# Test cases
print(remove_vowels("Cat"))        # Ct
print(remove_vowels("Computer"))   # Cmptr


# Sort a sentence based on numbers embedded in words

def sort_sentence(sentence):
    words = sentence.split()
    sorted_words = [""] * len(words)

    for word in words:
        for ch in word:
            if ch.isdigit():
                position = int(ch) - 1
                clean_word = word.replace(ch, "")
                sorted_words[position] = clean_word

    return " ".join(sorted_words)


# Test cases
print(sort_sentence("is1 Th0s T3est 2a"))  
# This is a Test

print(sort_sentence("t2o j3oin 4WonderBiz i0 Technolog5ies wan1t"))
# I want to join WonderBiz Technologies
