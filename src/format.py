import markdown

def save_as_update_html(results, start_date, end_date, authors=None, keywords=None, repositories=None, output_file="results.html"):
    """
    Save search results to an HTML file formatted with Markdown.

    Parameters:
    - results (list of dict): Search results with title, abstract, and URL.
    - output_file (str): Name of the output HTML file.
    """
    # Generate Markdown content
    md_content = "# Arχiv Weekly Update\n"
    md_content += f"#### {start_date.strftime('%a')} {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%a')} {end_date.strftime('%Y-%m-%d')}\n\n"
    md_content += "### Search Criteria\n"
    md_content += " - **Subject categories**: " + ", ".join(repositories)
    md_content += "\n - **Match authors**: " + ", ".join(authors)
    md_content += "\n - **Match abstract**: " + ", ".join(keywords)
    md_content += "\n\n\n"
    for idx, paper in enumerate(results, start=1):
        md_content += "\n---\n"
        md_content += f"### [{paper['title']}]({paper['url']})\n\n"
        md_content += f"**Authors:** {', '.join(map(str, paper['authors']))}\n\n"
        md_content += f"**Published:** {paper['published'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Last Updated:** {paper['updated'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"**Categories:** <u>{paper['primary_category']}</u>"
        other_categories = paper['all_categories']
        other_categories.remove(paper['primary_category'])
        # only filer for math.XX type categories.
        # some are numeric, and I don't know what they mean.
        other_categories = [item for item in other_categories if "." in item]
        if other_categories:
            md_content += ", " + ", ".join(other_categories)
        md_content += "\n\n"
        md_content += f"**Abstract:**\n\n{paper['abstract']}\n\n"

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content, extensions=["extra"])
    
    # Save to an HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Results saved to {output_file}")
