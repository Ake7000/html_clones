# html_clones
The goal of this project was to design an algorithm that groups different HTML documents based on their visual appearance. I was provided with a set of HTML files organized into four tiers. Each tier contains documents with small differences, but they look similar. The challenge was to develop a solution that would group together documents that are visually similar.

Approach
  My idea was to group the documents by combining their visual and textual similarities.
  
  1. Visual Similarity
    I used a headless browser (via Selenium) to render each HTML file and capture a screenshot. Then, I used the "imagehash" library to compute a perceptual hash for each screenshot. Finally, I compared these hashes using the Hamming distance and stored the similarity score in a similarity matrix.
  
  2. Textual Similarity
    I extracted the visible text from each HTML file and removed non-relevant elements (such as <script>, <noscript>, and <style> tags) using BeautifulSoup. The cleaned text is then vectorized using TF-IDF, and I computed the cosine similarity between the resulting vectors. In the end, we obtained a similarity matrix for text.
  
  3. Combined Similarity
    Since both aspects (visual and textual) are important, I combined the two similarity matrices using a weighted sum, giving the visual factor a much higher weight. This resulted in a final similarity matrix.
  
  4. Clustering
    Finally, I used the DBSCAN clustering algorithm on the similarity matrix to generate cluster labels, based on which I created the corresponding output.

System Architecture

  main.py:
    This module serves as the central coordinator for the entire process. It iterates through each tier folder, processing each HTML file (capturing screenshots, extracting text, calculating similarities), and finally clusters the files based on their similarity.It is important that the folder named "clones" exists in the same directory as the program, as this folder contains the HTML files organized into tier subfolders. Additionally, the program creates a folder named "Raspuns", which organizes the output by tier and by cluster for easy visualization of the results.
  
  screenshot.py:
    This module is responsible for launching a headless browser, loading the HTML files, and capturing screenshots.
  
  procesare_html.py:
    This module uses BeautifulSoup to parse HTML files, remove non-visible elements, and extract the visible text content.
  
  functii.py:
    This module implements the core similarity functions. It calculates the perceptual hash of images, compares screenshot hashes using Hamming distance, calculates textual similarity via TF-IDF and cosine similarity, and combines the two similarity matrices.
  
  clustering.py:
    This module contains the clustering algorithm using DBSCAN on the combined similarity matrix.

  
