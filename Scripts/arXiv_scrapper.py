# arxiv_scraper.py
import arxiv
import csv

# Parameters
query = 'cs.AI'  # Example: Computer Science > Artificial Intelligence
max_results = 1000  # Adjust as needed
output_file = 'arxiv_cs_dataset.csv'

# Search
results = arxiv.Search(
    query=query,
    max_results=max_results,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Write to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'title', 'abstract', 'authors', 'published', 'categories'])
    for result in results.results():
        writer.writerow([
            result.entry_id,
            result.title,
            result.summary.replace('\n', ' '),
            ', '.join(str(a) for a in result.authors),
            result.published.date(),
            ', '.join(result.categories)
        ])

print(f"Saved {max_results} entries to {output_file}")
