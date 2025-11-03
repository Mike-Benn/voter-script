"""import pdfplumber

pdf_path = "brown-co.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        print(f"--- Page {i} ---")
        print(text)
        print("\n")
        break
"""

import fitz
import csv

pdf_path = "brown-co.pdf"
csv_path = "results.csv"

print()
county_name = input("Enter county name (without 'County'): ").replace("County", "").strip()
county_name = county_name.lower()
print()

with fitz.open(pdf_path) as pdf, open(csv_path, "w", newline="") as doc:
    page = pdf[0]
    drawings = page.get_drawings()
    words = page.get_text("words")

    rects = [d['rect'] for d in drawings if 'rect' in d]
    rect_data = {}
    records_batch = []
    """for i, rect in enumerate(rects):
        x0, y0, x1, y1 = rect
        print(f"Rectangle {i}: x0={x0}, y0={y0}, x1={x1}, y1={y1}")"""

    for i, word in enumerate(words):
        word_x0, word_y0, word_x1, word_y1 = word[0], word[1], word[2], word[3]
        for j, rect in enumerate(rects):
            rect_x0, rect_y0, rect_x1, rect_y1 = rect
            if rect_x0 <= word_x0 <= rect_x1 and rect_y0 <= word_y1 <= rect_y1:
                if j not in rect_data:
                    rect_data[j] = [word]
                    break
                rect_data[j].append(word)
                break
    """
    for words in rect_data.values():
        if len(words) == 1:
            print()
            print(words[0][4])
            print()
            break
        words_to_print = f"{words[0][4]}"
        for i in range(1, len(words)):
            word = words[i]
            words_to_print += f" {word[4]}"
        print()
        print(words_to_print)
        print()
    """
    ######## Sorts header into blocks #########

    page_header = rect_data[0]
    sorted_blocks = []
    first_word = page_header[0]
    prev_x0 = first_word[0]
    prev_y1 = first_word[3]
    current_block = [first_word]
    
    for k in range(1, len(page_header)):
        current_word = page_header[k]

        # Same line check
        curr_x0 = current_word[0]
        curr_y1 = current_word[3]
        if 0 < curr_x0 - prev_x0 < 100 and abs(prev_y1 - curr_y1) < 1:
            current_block.append(current_word)
            prev_x0 = curr_x0
            prev_y1 = curr_y1
            continue
        # New line creation
        else:
            sorted_blocks.append(current_block)
            current_block = [current_word]
            prev_x0 = curr_x0
            prev_y1 = curr_y1
            continue
    
    """
    # Print sorted_blocks
    for block in sorted_blocks:
        line_text = f"{block[0][4]}"
        for m in range(1, len(block)):
            line_text += f" {block[m][4]}"
        print()
        print(line_text)
        print()
    """    

    # Get precinct name

    precinct_block = sorted_blocks[5]
    precinct_name = " ".join(word[4] for word in precinct_block)
    
    test_data = rect_data[1]
    test_data.sort(key=lambda x: (x[3], x[0]))


    for word in test_data:
        print()
        print(word)
        print()
    # Sort code blocks 
    for key, value in rect_data.items():
        if key == 0:
            continue
        sorted_block = rect_data[key].sort(key=lambda x: (x[3], x[0]))
        
        


        


    

    # Write to csv
    


    



    



        

    

    




    





    
