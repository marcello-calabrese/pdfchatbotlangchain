import nltk
from nltk.corpus import stopwords

def get_stopwords(language='english'):
    """
    Get a set of stopwords for the specified language.

    Parameters:
        language (str): The language for which to get the stopwords.
                        Default is 'english'.

    Returns:
        set: A set of stopwords for the specified language.
    """
    #nltk.download('stopwords') '''uncomment this line if you haven't downloaded the stopwords yet'''
    return set(stopwords.words(language))

# stopwords_set = get_stopwords('english ')

# if __name__ == '__main__':
#     print(stopwords_set)
    