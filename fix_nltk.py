# fix_nltk.py
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("Downloading NLTK resources...")

# Download semua resource yang diperlukan
resources = [
    'punkt',
    'stopwords', 
    'averaged_perceptron_tagger',
    'vader_lexicon'
]

for resource in resources:
    try:
        print(f"Downloading {resource}...")
        nltk.download(resource)
        print(f"✓ {resource} downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading {resource}: {e}")

print("\nNLTK setup completed!")