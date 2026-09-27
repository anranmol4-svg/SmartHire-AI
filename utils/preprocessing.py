import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are downloaded automatically on first run
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)

STOPWORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()

def clean_text(text: str, lemmatize: bool = True) -> str:
    """
    Cleans raw resume or JD text for TF-IDF vectorization.
    
    Args:
        text (str): Raw extracted text.
        lemmatize (bool): Whether to apply Lemmatization.
        
    Returns:
        str: Cleaned, normalized string.
    """
    if not text:
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs and Email addresses
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    
    # 3. Remove non-alphanumeric characters, keeping spaces, +, #, and . (for C++, C#, .NET)
    text = re.sub(r'[^a-zA-Z0-9\s+#.]', ' ', text)
    
    # 4. Tokenize and remove Stopwords / Apply Lemmatization
    tokens = text.split()
    cleaned_tokens = []
    
    for token in tokens:
        # Strip trailing dots or punctuation while preserving tech terms like '.net'
        clean_tok = token.strip(',;')
        
        if clean_tok not in STOPWORDS and len(clean_tok) > 1:
            if lemmatize:
                clean_tok = LEMMATIZER.lemmatize(clean_tok)
            cleaned_tokens.append(clean_tok)
            
    return " ".join(cleaned_tokens)