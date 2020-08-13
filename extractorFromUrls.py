from newsplease import NewsPlease
import json, logging, os


class extractorFromUrls():
    __filename = ""
    __media = ""

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.INFO)
    
    def config(self, filename, media):
        self.__filename = filename
        self.__media = media

    def extractorFunc(self):
        extract_list = []
        with open("./crawler_urls/" + self.__filename, "r") as f:
            load_list = json.load(f)
        num_news = len(load_list)
        for i in range(num_news):
            news_dict = {}
            if self.__media in load_list[i]['media']:
                extractor = NewsPlease.from_url(load_list[i]['url'])
                news_dict["title"] = load_list[i]['title']
                news_dict["media"] = load_list[i]['media']
                news_dict["date"] = load_list[i]['date']
                news_dict["url"] = load_list[i]['url']
                maintext = extractor.maintext
                if maintext and len(maintext) > 200:
                    news_dict["text"] = maintext
                else:
                    continue
                extract_list.append(news_dict)
            else:
                continue
            if (i + 1) % 10 == 0:
                self.toJson(extract_list)
                extract_list = []
        self.toJson(extract_list)
                
    def toJson(self, news_list):
        filepath = "./crawler_extracted/" + self.__filename
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                load_list = json.load(f)
                load_list = load_list + news_list
            with open(filepath, 'w') as fw:
                json.dump(load_list, fw)
                logging.info("output extracted news to exist file: " + str(filepath))
        else:
            with open(filepath, 'w') as fw:
                json.dump(news_list, fw)
                logging.info("create new file: " + str(filepath))

    def run(self):
        self.extractorFunc()

test = extractorFromUrls()
test.config("South China Morning Post_test.json", "South China Morning Post")
test.run()


