import html_processor

def get_website_text(html_text):
    """
    Keeps only the interesting parts of a webpage
    :param response:
    :return:
    """
    html_text = str(html_text)
    new_html_text = html_text.replace("\\n", "")
    new_html_text = new_html_text.replace("\\t", "")
    new_html_text = new_html_text.replace("\\r", "")
    new_html_text = new_html_text.replace("\\", "")
    new_html_text = new_html_text.replace("  ", "")
    new_html_text = new_html_text.replace("\\xa0", "")
    new_html_text = new_html_text.replace("\n", "")
    new_html_text = html_text.replace('\xa0', ' ')

    soup = html_processor.HtmlProcessor(new_html_text)
    paragraphs = soup.extract_paragraphs()
    return ' \n '.join(paragraph for paragraph in paragraphs if len(paragraph)>30)