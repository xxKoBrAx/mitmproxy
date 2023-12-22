#xxKoBrAx 2023
#github repo https://github.com/xxKoBrAx
#blog https://medium.com/@marcovit87

import mitmproxy.http
import dns.resolver

class Resolver:
    def __init__(self):
        self.file_path = input("Enter the path to save results: ")

    def response(self, flow: mitmproxy.http.HTTPFlow):
        self.resolv(flow)

    def resolv(self, flow: mitmproxy.http.HTTPFlow):
        target_domain = flow.request.url
        record_types = ["A", "CNAME", "MX", "NS", "SOA", "SRV", "TXT"] #other records: https://en.wikipedia.org/wiki/List_of_DNS_record_types
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["8.8.8.8", "8.8.4.4", #google
                        "208.67.222.222", "208.67.220.220", #OpenDNS
                        "209.244.0.3", "209.244.0.4", #Level 3 DNS
                        "199.85.126.10", "199.85.127.10", #Norton ConnectSafe
                        "1.1.1.1", "1.0.0.1", #Cloudfare
                        ]
        for record_type in record_types:
            try:
                answers = resolver.resolve(target_domain, record_type)
            except dns.resolver.NoAnswer:
                continue
            for rdata in answers:
                with open(f"{self.file_path}/mitmproxy_DNS.txt", "a") as f:
                    f.write(f"{record_type} records for {target_domain}:\n {rdata}\n\n")

addons = [Resolver()]
