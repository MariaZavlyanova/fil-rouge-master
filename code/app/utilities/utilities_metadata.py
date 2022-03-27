import arxiv
import json
import urllib.request as libreq

## Arxiv Extraction

def extract_authors_arxiv_list(list_arxiv_authors):
    list_authors = []
    for arxiv_author in list_arxiv_authors:
        # print(arxiv_author)
        list_authors.append(str(arxiv_author))
    return list_authors

def extract_published_date(arxiv_publication_date):
    return arxiv_publication_date.date()

def extract_list_categories(arxiv_list_catgories):
    list_categories = []
    for arxiv_author in arxiv_list_catgories:
        # print(arxiv_author)
        list_categories.append(str(arxiv_author))
    return list_categories



## JSON DataBase

# function to add to JSON
# TODO add the verification that the pdf does not exist already
def write_json(new_data, filename='pdf_metadata.json', category = 'Papers'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[category].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# Extract metadata pdf with one id_pdf
def metadata_pdf (pdf_id, filename = 'pdf_metadata.json'):
    # First we load existing data into a dict.
    with open(filename,'r+') as file:
        file_data = json.load(file)["Papers"]
    
    # Then we search the id_pdf
    for metadata_pdf in file_data:
        # Check first if the metadata already exists
        if pdf_id.lower() == metadata_pdf['id'].lower():
            # print(type(keyval))
            return metadata_pdf



## PDF Download
def pdf_dowload(pdf_url,folder_name):
    extraction_path = "{}{}.pdf".format(folder_name,pdf_url.split("/")[-1])
    libreq.urlretrieve(pdf_url, extraction_path)
    print("The pdf has been dowloaded to the path : {}".format(extraction_path))


## Alimenter le JSON avec l'API
def create_json_pdf(pdf_id):
    search = arxiv.Search(id_list=[pdf_id])
    result = next(search.results())

    pdf_metadata = {
            "id" : pdf_id,
            "authors" : extract_authors_arxiv_list(result.authors),
            "date" : str(extract_published_date(result.published)),
            "title" : result.title,
            "categories" : extract_list_categories(result.categories),
            "journal" : result.journal_ref,
            "doi" : result.doi,
            "url" : result.pdf_url,
            "references" :[]
    }

    write_json(pdf_metadata)


#Show all the keys of extracted pdfs
def all_keys(filename='pdf_metadata.json'):
    # open json file
    with open(filename,'r+') as file:
        file_data = json.load(file)["Papers"]
    
    extracted_pdf = []
    for metadata_pdf in file_data:

        extracted_pdf.append(metadata_pdf['id'])
    return extracted_pdf