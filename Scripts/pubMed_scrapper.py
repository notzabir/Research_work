# pubmed_scraper.py
from Bio import Entrez
import csv

# Required: Your email for NCBI access
Entrez.email = "your_email@example.com"

# Parameters
search_term = "cancer immunotherapy"
max_results = 1000
output_file = "pubmed_bio_dataset.csv"

# Search PubMed
handle = Entrez.esearch(db="pubmed", term=search_term, retmax=max_results)
record = Entrez.read(handle)
ids = record["IdList"]

# Fetch metadata
handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="xml")
papers = Entrez.read(handle)

# Save to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['pmid', 'title', 'abstract', 'authors', 'journal', 'pubdate'])
    for article in papers['PubmedArticle']:
        pmid = article['MedlineCitation']['PMID']
        article_data = article['MedlineCitation']['Article']
        title = article_data.get('ArticleTitle', '')
        abstract = article_data.get('Abstract', {}).get('AbstractText', [''])[0]
        authors = ', '.join([
            a['LastName'] + ' ' + a['ForeName']
            for a in article_data.get('AuthorList', [])
            if 'LastName' in a and 'ForeName' in a
        ])
        journal = article_data.get('Journal', {}).get('Title', '')
        pubdate = article_data.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {}).get('Year', '')
        writer.writerow([pmid, title, abstract, authors, journal, pubdate])

print(f"Saved {len(ids)} entries to {output_file}")
