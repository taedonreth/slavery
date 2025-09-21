# leetcode 1242: Web Crawler Multithreaded (medium)
# kind of finished not really

import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, wait
from typing import List

# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
# class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """


class Solution:
    def crawl(self, startUrl: str, htmlParser: "HtmlParser") -> List[str]:
        # single threaded
        """
        q = deque([startUrl])
        result = set([startUrl])  # set for unique visited links

        # extract hostname of startUrl
        idx = curr_link.find("/", curr_link.find("//") + 2)
        hostname = curr_link[:idx]

        # bfs version
        while q:
            curr_link = q.popleft()

            for link in htmlParser.getUrls(curr_link):
                if link.startswith(hostname) and link not in result:
                    result.add(link)
                    q.append(link)

        return list(result)
        """

        # extract hostname of startUrl
        idx = startUrl.find("/", startUrl.find("//") + 2)
        hostname = startUrl[:idx]

        result = set([startUrl])
        lock = threading.Lock()

        # dfs version
        def dfs(url: str) -> None:
            for link in htmlParser.getUrls(url):
                if link.startswith(hostname):
                    with lock:
                        if link not in result:
                            result.add(link)
                            futures.append(executor.submit(dfs, link))

        with ThreadPoolExecutor() as executor:
            futures.append(executor.submit(dfs, startUrl))
            # wait for ALL futures to complete
            wait(futures)

        return list(result)


def main():
    sol = Solution()

    # Example 1
    urls1 = [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.google.com",
        "http://news.yahoo.com/us",
    ]
    edges1 = [[2, 0], [2, 1], [3, 2], [3, 1], [0, 4]]
    startUrl1 = "http://news.yahoo.com/news/topics/"
    parser1 = HtmlParser(edges1, urls1)
    output1 = sol.crawl(startUrl1, parser1)
    expected1 = [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.yahoo.com/us",
    ]
    assert set(output1) == set(expected1)

    # Example 2
    urls2 = [
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/news/topics/",
        "http://news.google.com",
    ]
    edges2 = [[0, 2], [2, 1], [3, 2], [3, 1], [3, 0]]
    startUrl2 = "http://news.google.com"
    parser2 = HtmlParser(edges2, urls2)
    output2 = sol.crawl(startUrl2, parser2)
    expected2 = ["http://news.google.com"]
    assert set(output2) == set(expected2)

    print("All test cases passed!")


if __name__ == "__main__":
    main()
