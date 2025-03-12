import numpy as np
import imagehash
from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def hash_screenshot(screenshot_path):

    #calculating the screenshot hash
    screenshot = Image.open(screenshot_path)
    return imagehash.phash(screenshot)

def comparare_ss(hash1, hash2):

    #calculating the Hamming distance for two image hashes and converting it into a similarity score
    distanta = hash1 - hash2
    distanta_max = 64
    asemanare = 1 - (distanta / distanta_max)
    return asemanare

def comparare_text(texts):

    #calculating the similarity matrix for a list of texts
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(texts)
    asemanari = cosine_similarity(tfidf)
    return asemanari

def combinare_asemanari(asemanari_ss, asemanari_text, weight_ss, weight_text):

    #calculating the combined similarity matrix obtained from screenshot and text similarity matrices
    return weight_ss * asemanari_ss + weight_text * asemanari_text