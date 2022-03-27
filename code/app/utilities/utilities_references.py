import json
from refextract import extract_references_from_url
from utilities.utilities_metadata import metadata_pdf
from utilities.utilities_metadata import all_keys, write_json
import spacy


# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_md")
except: # If not present, we download
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

#get the url from a pdf stored in the JSON file created with the API
def get_url_from_id(pdf_id):
    # open json file
    # find the pdf that we want
    pdf = metadata_pdf(pdf_id)
    url_pdf = pdf["url"]
    return url_pdf

# Create a list of references that can be found in one pdf, 
# with the url of one pdf
def extract_authors(url_pdf):
    # Extract references from pdf_url
    # using refextract library
    references = extract_references_from_url(url_pdf)

    # create a list where we will put all extracted authors
    authors_extracted = []

    #Extract authors form each line of reference
    for ref in references:
        # store the raw reference
        raw_reference = str(ref['raw_ref'])
        # label each word of the reference
        nlp_extraction = nlp(raw_reference)
        # extract only the PERSON label
        list_authors_one_ref = [str(ee) for ee in nlp_extraction.ents if ee.label_ == 'PERSON']
        # store the authors in the commun list
        dic_references = {
                            "id" : "{}".format(url_pdf.split("/")[-1]),
                            "raw_ref" : raw_reference, 
                            "list_authors" : list_authors_one_ref}

        authors_extracted.append(dic_references)

    return authors_extracted


# Store extracted list of pdf in a text file
def store_list_authors_txt(list_authors, pdf_id):
    with open("extracted_authors/{}_authors.txt".format(pdf_id), "w") as output:
        output.write(str(list_authors))

## Alimenter le JSON des references avec l'API
def create_json_referenes(pdf_id):
    url_pdf = get_url_from_id(pdf_id)
    extracted_reference=extract_authors(url_pdf)
    # print(extracted_reference)
    write_json(extracted_reference, filename = 'pdf_references.json', category = 'References')

# Extract references pdf with one id_pdf
def references_pdf (pdf_id, filename = 'pdf_references.json'):
    # First we load existing data into a dict.
    with open(filename,'r+') as file:
        file_data = json.load(file)["References"]
    output = []
    # Then we search the id_pdf
    for references in file_data:
        # Check first if the metadata already exists
            output.append([references_pdf for references_pdf in references if pdf_id.lower() == references_pdf['id'].lower()])

    return output