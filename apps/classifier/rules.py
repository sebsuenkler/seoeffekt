import sys
sys.path.insert(0, '..')
from include import *


def classify(classifier_id, hashes):



    def check_title(tree):

        title = ""

        xpath_title = "//title/text()"
        xpath_meta_title = "//meta[@name='title']/@content"
        xpath_og_title = "//meta[@property='og:title']/@content"

        check_title = str(tree.xpath(xpath_title))
        check_meta_title = str(tree.xpath(xpath_meta_title))
        check_og_title = str(tree.xpath(xpath_og_title))

        if len(check_title) > 4 or len(check_meta_title) > 4  or len(check_og_title) > 4:
            if len(check_og_title) > 4:
                title = check_og_title
            elif len(check_meta_title) > 4:
                title = check_meta_title
            else:
                title = check_title

            title = title[2:-2]

            title = title.replace("'", "")
            title = title.replace('"', "")
            title = title.replace(':', "")
            title = title.replace(',', "")

            title = title.strip()


        return title

    def check_identical_title(hash):
        results_urls = str(Sources.getSourcesURLs(hash))

        list_results_urls = list(results_urls.split("[url]"))

        results_links = []

        for l in list_results_urls:
            url_split = l.split("   ")
            try:
                if results_main in url_split[1]:
                    if not Helpers.matchText(url_split[1], '*javascript*') and not Helpers.matchText(url_split[1], '*None*') and url_split[1] != results_main and Helpers.validate_url(url_split[1]):
                        results_links.append(url_split[1])
            except:
                pass


        results_links = list(dict.fromkeys(results_links))

        number_of_links = 2
        n = 0

        if len(results_links) < number_of_links:
            number_of_links = len(results_links)

        results_source = Results.getResultsSource(hash)
        code = Helpers.html_unescape(results_source[0][0])
        code = code.lower()
        tree = html.fromstring(code)

        title = check_title(tree)

        identical_title = 0


        while n < number_of_links and number_of_links < 5:
            try:
                print(results_links[n])
                source = Results.saveResult(results_links[n])
                if source != 'error':
                    n += 1
                    code = source.lower()
                    tree = html.fromstring(code)
                    link_title = check_title(tree)
                    if title == link_title:
                        identical_title = 1
                else:
                    number_of_links += 1

            except:
                number_of_links += 1


        return identical_title


    for h in hashes:

        hash = h[0]
        results_url = h[1]
        results_main = h[2]
        results_speed = h[3]



        evaluations_results = Evaluations.getEvaluationsResults(hash)

        dict_results = {}

        for e in evaluations_results:
            evaluations_module =  e[0]
            evaluations_result = e[1]

            #indicators for rule based classification
            dict_results.update({evaluations_module: evaluations_result})

        #convert dict elements for rule based classification

        #sources:
        source_not_optimized = int(dict_results['source not optimized'])
        source_news = int(dict_results['source news'])
        source_known = int(dict_results['source known'])
        source_search_engine = int(dict_results['source search engine'])
        source_shop = int(dict_results['source shop'])
        source_top = int(dict_results['source top'])
        source_ads = int(dict_results['source ads'])
        source_company = int(dict_results['source company'])

        #indicators:
        indicator_https = int(dict_results['check https'])
        indicator_robots_txt = int(dict_results['robots_txt'])
        indicator_sitemap = int(dict_results['check sitemap'])
        indicator_nofollow = int(dict_results['check nofollow'])
        indicator_speed = float(results_speed)
        indicator_canonical = int(dict_results['check canonical'])
        indicator_viewport = int(dict_results['check viewport'])
        indicator_og = int(dict_results['check og'])
        indicator_micros = int(dict_results['micros counter'])
        indicator_title = int(dict_results['check title'])
        indicator_description = int(dict_results['check description'])
        indicator_speed = results_speed

        #plugins and tools
        tools_analytics = int(dict_results['tools analytics count'])
        tools_seo = int(dict_results['tools seo count'])
        tools_caching = int(dict_results['tools caching count'])
        tools_content = int(dict_results['tools content count'])
        tools_social = int(dict_results['tools social count'])
        tools_ads = int(dict_results['tools ads count'])

        #classification
        classification_count = 0
        not_optimized = 0
        optimized = 0
        probably_optimized = 0
        probably_not_optimized = 0
        classification_result = "uncertain"
        indicator_identical_title = 0

        #most_probably_not_optimized
        if source_not_optimized == 1:
            not_optimized = 1
            classification_result = 'not optimized'
            classification_count += 1

        #most probably optimized
        if not_optimized == 0 and (tools_seo > 0 or source_known == 1 or source_news == 1 or source_ads == 1 or indicator_micros > 0):
            optimized = 1
            classification_result = 'optimized'
            classification_count += 1

        #probably optimized
        if optimized == 0 and not_optimized == 0 and (tools_analytics > 0 or source_shop == 1 or source_company == 1 or indicator_https == 1 or indicator_og == 1 or indicator_viewport == 1 or indicator_robots_txt == 1 or indicator_sitemap == 1 or indicator_nofollow > 0 or indicator_canonical > 0 or (indicator_speed < 3 and indicator_speed > 0)):
            probably_optimized = 1
            classification_result = 'probably_optimized'
            classification_count += 1

        if optimized == 0 and not_optimized == 0 and probably_optimized == 0:
            indicator_identical_title = check_identical_title(hash)

        #probably_not_optimized
        if optimized == 0 and not_optimized == 0:
            if indicator_title == 0 or indicator_description == 0 or indicator_identical_title == 1:
                probably_not_optimized = 1
                classification_result = 'probably_not_optimized'
                classification_count += 1

        #if classification_count == 0 or classification_count > 1:
        #    classification_result = "uncertain"

        #elif probably_optimized == 1 and probably_not_optimized == 1:
        #    classification_result = "uncertain"


        if (not Evaluations.getClassificationResult(hash, classifier_id)):
            Evaluations.insertClassificationResult(hash, classification_result, classifier_id, today)
            print(results_url)
            print(hash)
            print(classification_result)
