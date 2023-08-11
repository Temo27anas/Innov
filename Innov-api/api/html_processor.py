from bs4 import Comment
from bs4 import BeautifulSoup

class HtmlProcessor():
    def __init__(self, page_html: str = None) -> None:
        """
        Constructor for class Process
        @param page_url: page to process
        @param page_html: html of the page to process
        """
        self.soup = BeautifulSoup(page_html, features='html.parser')

    def remove_tags(self, tags: list) -> None:
        """
        Remove tags completely from HTML
        @param tags: list of tags that contains elements to remove
        """
        for script in self.soup(tags):
            script.decompose()

    def unwrap_tags(self, tags: list) -> None:
        """
        unwrap tags from html
        ex: if we want to unwrap the element <i>, this code "<p>Hello <i>World</i></p>" will become "<p>Hello World</p>"
        @param tags: list of tags that contains elements to unwrap
        """
        for script in self.soup(tags):
            script.unwrap()

    # TODO: Test this function
    def remove_comments(self) -> None:
        """
        Remove all comments <!-- --> from html
        """
        for comment in self.soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

    def translate_line_breaks(self) -> None:
        """
        Cleans HTML by removing comments and useless scripts like script, style or tags
        """
        for i in self.soup.select("br"):  # replace br by \n so we can split by n
            i.replace_with("\n")

    def clean_html(self) -> None:
        """
        Cleans HTML by removing comments and useless scripts like script, style or tags
        """
        self.remove_tags(["script", "style", "link"])
        self.remove_comments()
        self.translate_line_breaks()

    # TODO: check if there are duplicates
    def extract_paragraphs(self):
        """
        Method that returns all the paragraphs and sentences from an HTMl page by applying all necessary cleaning methods
        @return: Returns dict that contains the page url and the extracted sentences
        """
        sentences = set()
        tags_to_extract = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        self.unwrap_tags(['strong', 'i', 'b', 'u', 'a', 'em'])

        for tag in tags_to_extract:  # Loop through a list of elements so that we can take the whole block
            paragraphs = [sentence.strip() for temp in self.soup([tag]) for sentence in temp.text.split('\n') if
                            sentence.strip()]  # split paragraphs by new line
            sentences.update(paragraphs)
        return sentences
