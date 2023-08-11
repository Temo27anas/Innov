import config
import json

# Read the json file
def read_json(path):
    with open(path, encoding="utf8") as f:
        return json.load(f)

#
languages = []
for language in config.languages:
    language_dict = read_json(config.root_path + language + ".json")
    languages += language_dict["sublinks"]

# Remove duplicates
keywords_in_link_to_check_in = list(set(languages))

# unwanted links
keywords_in_link_to_remove = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.mpg', '.mpeg', '.exe', '.avi', '.mov', '.wmv',
                              '.rm', '.ram', '.swf', '.flv', '.ogg', '.webm', '.mp4', '.pkg', '.mid', '.wma', '.aac', '.wav',
                              '.mp3', '.psd', '.xcf', '.cdr', '.tif', '.bmp', '.jpg', '.jpeg', '.img', '.AppImage', '.gif', '.png',
                              '.eps', '.raw', '.cr2', '.nef', '.orf', '.zip', '.7z', '.rar', '.tar.', '.tgz', '.tbz2',
                              '.txz', '.sr2', '.vcf', '.sr2', '.vcf', 'mailto:', 'tel:', 'facebook', 'twitter', 'instagram', 'linkedin',
                              'snapchat', 'pinterest', 'youtube', 'indeed', 'vimeo', 'viadeo', 'dailymotion', 'download',
                              'telechar', 'torrent', 'media', "news", "blog", "actualité"]
