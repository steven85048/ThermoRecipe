from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk

from model.load import load_id_range
from model.text_cleaning_utils import remove_punctuation

nltk.download('popular')
stop_words = set(stopwords.words("english"))

MIN_ID = 480
MAX_ID = 500
recipe_df, reviews_df, ingredients_df = load_id_range(MIN_ID, MAX_ID)

print(recipe_df[recipe_df.id == 483])
print(ingredients_df[ingredients_df.recipe_id == 483].ingredient)
print(reviews_df[reviews_df.recipe_id == 483])

ingredients = ingredients_df[ingredients_df.recipe_id == 483].ingredient
for ingredient in ingredients:
    # Missed bug during scraping
    if(ingredient == "Add all ingredients to list"):
        continue

    ingredient = remove_punctuation(ingredient)
    ingredient_tok = word_tokenize(ingredient)
    print(nltk.pos_tag(ingredient_tok))

'''
def filter_stopwords(words, stop_words):
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return filtered_words

for description in descriptions:
    tokenized_text = sent_tokenize(description)
    for sentence in tokenized_text:
        words = word_tokenize(sentence)
        print(nltk.pos_tag(words))
        filtered_words = filter_stopwords(words, stop_words)

        #print(sentence)
        #print(filtered_words)
'''