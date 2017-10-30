#!usr/bin/python
from lollygag import LinkParser, run, Services

INTERESTING = ['fantasy', 'romance']


class BookParser(LinkParser):

    def __init__(self, *args, **kwargs):
        super(LinkParser, self).__init__(*args, **kwargs)
        self.isGenreLink = False
        self.url = None
        self.found = []

    def parse(self, url):
        self.url = url
        result = super(BookParser, self).parse(url)
        if self.found:
            with open('result.txt', 'a') as outfile:
                outfile.write('%s    %s\n' % (self.url, self.found))
        return result

    def handle_starttag(self, tag, attrs):
        super(BookParser, self).handle_starttag(tag, attrs)
        if tag == 'a' and ('class', 'actionLinkLite bookPageGenreLink') in attrs:
            self.isGenreLink = True

    def handle_data(self, data):
        if self.isGenreLink:
            lower_data = data.lower()
            self.log_service.important(lower_data)
            if lower_data in INTERESTING:
                self.found.append(lower_data)

    def handle_endtag(self, tag):
        if self.isGenreLink and tag == 'a':
            self.isGenreLink = False


def main():
    Services.site_parser_factory = BookParser
    run(url="https://www.goodreads.com/search?q=romance")


if __name__ == '__main__':
    main()
