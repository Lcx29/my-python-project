from feature.article.support.base_article_crawler import ArticleCrawler
from feature.article.support.csdn_crawler import CSDNCrawler
from feature.article.support.jianshu_crawler import JianshuCrawler
from feature.article.support.juejin_crawler import JuejinCrawler
from feature.article.support.zhihu_crawler import ZhihuCrawler

prog = "article_crawler"
description = "A package for crawling markdown formatted articles from certain webpage and storing them locally."
version = '0.0.1'
usage = "python3 -m article_crawler -u [url] -t [type] -o [output_folder] -c [class_] -i [id]"

class_dic = {
    "csdn": CSDNCrawler,
    "jianshu": JianshuCrawler,
    "juejin": JuejinCrawler,
    "zhihu": ZhihuCrawler
}


def main():
    url = options.url
    type = options.type
    output_folder = options.output_folder
    website_tag = options.website_tag
    class_ = options.class_
    id = options.id
    if not url:
        parser.error("url must be specified.")
    if not output_folder:
        parser.error("output folder must be specified.")
    if type == "" and website_tag == "" and class_ == "" and id == "":
        parser.error("'type', 'website_tag', 'class_', 'id' cannot be empty at the same time.")
    if type != '':
        if type not in ["csdn", "juejin", "zhihu", "jianshu"]:
            parser.error(
                "The current article type is not supported, you need to specify 'class_' or 'id' to locate the position of the article.")
        crawler = class_dic[type](url=url, output_folder=output_folder)
    else:
        crawler = ArticleCrawler(url=url, output_folder=output_folder, tag=website_tag, class_=class_, id=id)
    crawler.start()


if __name__ == '__main__':
    from optparse import OptionParser
    # https://juejin.cn/post/7263840667826323493
    # -u https://juejin.cn/post/7326923332196237351 -o /Users/lcn/Downloads/note -t juejin
    parser = OptionParser(prog=prog, description=description, version='%prog ' + version, usage=usage)
    parser.add_option("-u", "--url", dest="url", help="crawled url (required)")
    parser.add_option("-t", "--type", dest="type", default="",
                      help="crawled article type [csdn] | [juejin] | [zhihu] | [jianshu]")
    parser.add_option("-o", "--output_folder", dest="output_folder",
                      help="output html / markdown / pdf folder (required)")
    parser.add_option("-w", "--website_tag", dest="website_tag",
                      help="position of the article content in HTML (not required if 'type' is specified)")
    parser.add_option("-c", "--class", dest="class_", default="",
                      help="position of the article content in HTML (not required if 'type' is specified)")
    parser.add_option("-i", "--id", dest="id", default="",
                      help="position of the article content in HTML (not required if 'type' is specified)")
    options, args = parser.parse_args()
    main()
