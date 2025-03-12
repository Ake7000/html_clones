import os
import shutil
import numpy as np
from screenshot import poza_screenshot
from procesare_html import parse_html
from clustering import grupare
import matplotlib.pyplot as plt
from functii import hash_screenshot, comparare_ss, comparare_text, combinare_asemanari

def procesare_tier_folder(tier_folder):
    #getting the list of HTML files
    html_files = [f for f in os.listdir(tier_folder) if f.endswith('html')]

    #creating the directory where the screenshots will be saved
    screenshots_dir = os.path.join(tier_folder, "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

    texts = []      #text extracted from HTML files list
    ss_hashes = []  #screenshot hash list

    for file in html_files:
        
        file_path = os.path.join(tier_folder, file)
        screenshot_path = os.path.join(screenshots_dir, file + ".png")

        #taking a screenshot of the website if it does not exist
        if not os.path.exists(screenshot_path):
            poza_screenshot(file_path, screenshot_path)

        #extracting filtered text from each HTML document
        text = parse_html(file_path)
        texts.append(text)

        #calculating the screenshot hash for future comparison
        ss_hash = hash_screenshot(screenshot_path)
        ss_hashes.append(ss_hash)

    n = len(html_files)

    #calculating the similarity matrix for screenshots
    asemanari_ss = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            asemanare = comparare_ss(ss_hashes[i], ss_hashes[j])
            asemanari_ss[i][j] = asemanare

    #calculating the similarity matrix for text
    asemanari_text = comparare_text(texts)

    #calculating the combined similarity matrix with specific weights
    weight_ss = 0.8
    weight_text = 0.2
    asemanari_combinate = combinare_asemanari(asemanari_ss, asemanari_text, weight_ss, weight_text)
    
    #creating labels for clustering
    eps = 0.39
    min_samples = 1
    labels = grupare(asemanari_combinate, eps, min_samples)

    #clustering the HTML documents based on the labels
    clusters = {}
    for label, file in zip(labels, html_files):
        clusters.setdefault(label, []).append(file)
    
    for label, files in clusters.items():
        print("Grup", label, ":", files)

    #Creating an output file for easy visualization by saving the clustered documents in their specific subdirectories 
    save_cluster_images(tier_folder, labels, html_files)


def save_cluster_images(tier_folder, labels, html_files):

    tier_name = os.path.basename(tier_folder)
    output_root = "Raspuns"
    os.makedirs(output_root, exist_ok=True)
    
    #creating a subdirectory for the specific tier
    tier_output = os.path.join(output_root, f"Raspuns_{tier_name}")
    os.makedirs(tier_output, exist_ok=True)
    
    #creating group folders for each label and saving the screenshots
    for label, file in zip(labels, html_files):
        group_name = f"Grupa_{label + 1}"
        
        group_dir = os.path.join(tier_output, group_name)
        os.makedirs(group_dir, exist_ok=True)
        
        screenshot_path = os.path.join(tier_folder, "screenshots", file + ".png")
        dest_path = os.path.join(group_dir, file + ".png")
        
        shutil.copy(screenshot_path, dest_path)

def main():
    
    #creating the ouput folder each time the program runs
    output_root = "Raspuns"
    if os.path.exists(output_root):
        shutil.rmtree(output_root)

    main_folder = "clones"
    tiers = ["tier1", "tier2", "tier3", "tier4"]

    #going through each tier folder
    for tier in tiers:
        tier_folder = os.path.join(main_folder, tier)
        if os.path.exists(tier_folder):
            print("\nProcesăm folderul:", tier_folder)
            procesare_tier_folder(tier_folder)
        else:
            print("Folderul", tier_folder, "nu există.")

if __name__ == "__main__":
    main()