"""
Ce code permet d'initialiser le dataset JSON
Au debut du lancement il est possible d'initiliser en lancant :
    $ python dataset.py
il sera necessaire de choisir la taille du dataset (Cf le commentaire)
"""

import arxiv
from utilities.utilities_metadata import extract_authors_arxiv_list, extract_published_date, extract_list_categories
from utilities.utilities_metadata import write_json

# pdf mining from arxiv library
search = arxiv.Search(
    # taking only the subjects Computer Science and AI
    query = "cat:cs.AI",
    max_results = 200, #change number of pdf files that we want to extract
    sort_by = arxiv.SortCriterion.SubmittedDate
)


for result in search.results():
    id_pdf = result.entry_id.split("/")[-1]


    # Extracting metadata from the pdf

    pdf_metadata = {
        "id" : id_pdf,
        "authors" : extract_authors_arxiv_list(result.authors),
        "date" : str(extract_published_date(result.published)),
        "title" : result.title,
        "categories" : extract_list_categories(result.categories),
        "journal" : result.journal_ref,
        "doi" : result.doi,
        "url" : result.pdf_url,
        "references" :[]
    }


    # add metadata to the json file
    write_json(pdf_metadata)


