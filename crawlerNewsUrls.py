from json import load
from time import time
from typing import KeysView
from GoogleNews import GoogleNews
from newsplease import NewsPlease
from datetime import date, datetime, timedelta

import json, logging, os


class crawlerNewsUrls():
    __dateTime = ""
    __keyWords = ""
    __numDays = 0
    __pagsEveryDay = 0
    __daysSpan = 0

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.DEBUG)

    def config(self, dateTime, keyWords, numDays, pagsEveryDay, daysSpan):
        self.__dateTime = dateTime
        self.__keyWords = keyWords
        self.__numDays = numDays
        self.__pagsEveryDay = pagsEveryDay
        self.__daysSpan = daysSpan

    def toJson(self, googleNews):
        news_list = []
        startDay = self.__dateTime
        endDay = startDay + timedelta(days=self.__numDays - 1)
        if len(googleNews):
            for news in googleNews:
                page = {}
                page["title"] = news['title'].replace('\u2019', '\'').replace('\u2019', '\'')
                page["media"] = news['media']
                page["date"] = news['date'].replace('\u5e74', '.').replace(
                    '\u6708', '.').replace('\u65e5', '.')
                page["url"] = news['link']
                news_list.append(page)

            filename = "./crawler_urls/" + self.__keyWords + '_news_' + str(
                startDay.date()) + '_To_' + str(endDay.date()) + '.json'

            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    load_list = json.load(f)
                    load_list = load_list + news_list
                with open(filename, 'w') as fw:
                    json.dump(load_list, fw)
                    logging.info("output to exist file: " + str(filename))
            else:
                with open(filename, 'w') as fw:
                    json.dump(news_list, fw)
                    logging.info("create new file: " + str(filename))

    def googleNewsCrawler(self):
        result_list = []
        googlenews = GoogleNews()

        for i in range(self.__numDays):
            startDateTime = self.__dateTime + timedelta(days=i)
            endDateTime = self.__dateTime + timedelta(days=i + self.__daysSpan)

            googlenews.setTimeRange(
                start=str(startDateTime.month) + '/' + str(startDateTime.day) +
                '/' + str(startDateTime.year),
                end=str(endDateTime.month) + '/' + str(endDateTime.day) + '/' +
                str(endDateTime.year))
            googlenews.search(self.__keyWords)
            for j in range(self.__pagsEveryDay - 1):
                googlenews.getpage(j + 2)
            logging.info(
                str(self.__keyWords + '__' + str(startDateTime.date()) +
                    " append " + str(int(self.__pagsEveryDay * 10)) +
                    " items"))
            result_list = result_list + googlenews.result()
            googlenews.clear()

            if (i + 1) % 10 == 0:
                self.toJson(result_list)
                result_list = []
                continue
        self.toJson(result_list)


news = crawlerNewsUrls()
news.config(datetime(2020, 2, 26), 'BBC News', 165, 3, 0)
news.googleNewsCrawler()
