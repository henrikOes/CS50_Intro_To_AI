import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #set of all links
    links = set()
    for key, values in corpus.items():
        for value in values:
            if(value not in links):
                links.add(value)
    
    my_dict = {key: 0 for key in links}
    curr_page = page
    
    choices = list(corpus[curr_page])  # Get the list of choices for the current key
    other_choices = list(set(corpus.keys()))  # Get the other keys in the dictionary
    total_choices = choices + other_choices  # Combine both the choices

    # Assign probabilities
    probabilities = [damping_factor / len(choices)] * len(choices)  # Equal probability for the choices in the current key
    probabilities += [(1-damping_factor)/ len(other_choices)] * len(other_choices)  # Equal probability for the other keys

    # Choose randomly based on the weighted probabilities
    key = random.choices(total_choices, weights=probabilities, k=1)[0]

    #updates curr_page based on new key and adds 1/Samples to hits
    my_dict[key] += 1

    return my_dict
        


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    #Random start page
    links = list(set(corpus.keys()))
    probabilities = [1/len(links)] * len(links)
    page = random.choices(links, weights = probabilities, k=1)[0]
    start_dict = transition_model(corpus, page, damping_factor)
    
    for i in range(0, n-1):
        new_dict = transition_model(corpus, page, damping_factor)
        for key, value in new_dict.items():
            if value == 1:
                page = key
                start_dict[key] += 1
        
    for key, value in start_dict.items():
            start_dict[key] = value/n    
    
    print(start_dict)
    return start_dict
        


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    

if __name__ == "__main__":
    main()
