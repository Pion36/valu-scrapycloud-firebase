#encoding: utf-8
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor


from myproject.items import Genre #ItemのGenreクラスをインポート。

class ValuCrawlSpider(CrawlSpider):
    name = 'valu_crawl' #Spiderの名前。
    # クロール対象とするドメインのリスト。
    allowed_domains = ['valu.is']
    # クロールを開始するURLのリスト。1要素のタプルの末尾にはカンマが必要。
    start_urls = ('https://valu.is/users/categories?page=1','https://valu.is/users/categories?page=2','https://valu.is/users/categories?page=3')

    # リンクをたどるためのルールリスト。
    rules = (
        # ジャンルのページへのリンクをたどり、レスポンスをparse_genre()メソッドで処理する
        Rule(LinkExtractor(allow=r'/categories/\d+$')),
        Rule(LinkExtractor(allow=r'type=0&page=\w'),callback='parse_genre',follow=True),
    )

    # def parse(self, response):
    #     """
    #      トップページからピックアップのページへのリンクを抜き出してたどる。
    #     """
    #     # print(response.css('section.valuer_category a::attr("href")').extract())
    #     for url in response.css('section.valuer_category a::attr("href")').extract():
    #         yield scrapy.Request(url,self.parse_genre)

    def parse_genre(self, response):
        for i in range(len(response.css('div.ranking_info_box'))):
            item = Genre() # Genreオブジェクトを作成。
            item['name'] = response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+ str(i+1) +') > div.ranking_info_box > div.ranking_valuer_right > b::text').extract_first()
            item['jika'] = float(response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+ str(i+1) +') > div.ranking_info_box > div.ranking_valuer_left > b::text').extract_first().replace(',','').replace('\n',''))
            url = response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+ str(i+1) +') > div.ranking_info_box > a::attr(href)').extract_first()
            valuid = url[16:]
            item['url'] = url
            item['valuid'] = valuid
            item['imgurl'] = response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+ str(i+1) +') > div.ranking_valuer_pic::attr(style)').extract_first().split('(')[1].split(')')[0]
            item['genrename'] = response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+ str(i+1) +') > div.ranking_info_box > div.ranking_valuer_right > div > div.tag_type > a > span::text').extract_first()
            item['genrenum'] = int(response.css('#wrap > article > div > section.ranking_valuer > div:nth-child('+  str(i+1) +') > div.ranking_info_box > div.ranking_valuer_right > div > div.tag_type > a::attr(href)').extract_first().split('/')[5])
            if len(response.css('#wrap > article > div > section.ranking_valuer > div:nth-child(' + str(i+1) + ') > span')) == 1:
                item['treatment'] = 1
            else:
                item['treatment'] = 0
            yield item # Itemをyieldして、データを抽出する。
