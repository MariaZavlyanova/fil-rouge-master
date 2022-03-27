"""
Ce code permet de creer un JSON contenant les references
pour les pdf qui ont ete extrait precedement avec dataset.py
Au debut du lancement il est possible d'initiliser en lancant :
    $ python references.py
"""

from utilities.utilities_references import extract_authors, get_url_from_id, all_keys, write_json
from timeit import default_timer as timer

start_global = timer()

# import list of IDs
list_id = all_keys()

for pdf_id in list_id:
    start = timer()
    url_pdf = get_url_from_id(pdf_id)
    extracted_reference=extract_authors(url_pdf)
    # print(extracted_reference)
    write_json(extracted_reference, filename = 'pdf_references.json', category = 'References')
    # print(type(url_pdf))
    end = timer()
    print(end - start)


end_global = timer()
print(end_global - start_global) # Time in seconds, e.g. 5.38091952400282
