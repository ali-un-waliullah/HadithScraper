from fetch_collections import fetch_page, get_collections
from process_collections import parse_file, get_hadiths, check_pages
import os
import click


@click.group()
def cli():
    pass


def clear_collections():
    """
    Deletes all files in collections directory
    """
    collections = os.listdir("./collections")
    for c in collections:
        os.remove(f"./collections/{c}")


def get_files_in_pages() -> list:
    """
    Returns a list of files in pages directory
    """
    pages = []
    for dirpath, dirnames, filenames in os.walk('./pages'):
        for filename in filenames:
            pages.append(os.path.join(dirpath, filename))
    return pages


def parse_collectioins():
    pages = get_files_in_pages()
    print(pages)
    for p in range(0, len(pages)):
        soup = parse_file(pages[p])
        hadiths = get_hadiths(soup)
        with open(f"./collections/{p}.json", "w") as f:
            f.write(hadiths)
    # delete all files in pages directory
    for page in pages:
        os.remove(page)


@cli.command()
@click.argument('query', type=click.STRING, required=True)
@click.option('-o', '--output', is_flag=True, help="Save the output to a file")
def search(query: str, output: bool):
    """
    Fetches the search results for the given query and saves it to a file.
    """
    clear_collections()
    if query:
        if os.listdir("./pages"):
            click.echo("Pages already fetched. Skipping...", color="yellow")
        else:
            get_collections(query)
            soup = parse_file('./pages/search.html')
            pages = check_pages(soup)
            if pages:
                for p in range(0, len(pages)):
                    fetch_page(pages[p], f"search_{p}.html")
            click.echo("Pages fetched successfully.", color="green")
    if output:
        parse_collectioins()
        click.echo("Collections parsed successfully.", color="green")


cli.add_command(search)

if __name__ == "__main__":
    cli()
