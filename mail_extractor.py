#xxKoBrAx 2023
#github repo https://github.com/xxKoBrAx
#blog https://medium.com/@marcovit87

import mitmproxy.http
import re
from bs4 import BeautifulSoup as bs

class EmailExtractor:
    def __init__(self):
        self.file_path = input("Enter the path to save results: ")
        self.mail_patterns = [
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\.[A-Z|a-z]+',
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\.[A-Z|a-z]+\.[A-Z|a-z]+'
        ]

    def response(self, flow: mitmproxy.http.HTTPFlow):
        self.mail_extractor(flow)

    def mail_extractor(self, flow: mitmproxy.http.HTTPFlow):
        url = flow.request.url
        html = flow.response.text
        soup = str(bs(html,'html.parser').body)
        for pattern in self.mail_patterns:
            emails = re.findall(pattern,soup)
            emails_set= set(emails)
            with open(f"{self.file_path}/mitmproxy_mails.txt", "a") as f:
                if emails_set:
                    f.write(f"{url}\n{emails_set}\n\n")
                else:
                    f.write(f"{url}\n Nothing here\n\n")

addons = [EmailExtractor()]