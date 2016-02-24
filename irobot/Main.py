# coding: utf-8
__author__ = 'glcsnz123'
import re
import urllib, urllib2
import logging, os

BaseSite = "http://www.tianqihoubao.com/"


def _get_last_key_name(url):
    return url.split("/")[-1].split(".ht")[0]


def _get_re_list(content, pattern_string):
    patten = re.compile(pattern_string)
    return patten.findall(content)


def fetch_html(url="http://explosm.net/comics/1001/"):
    try:
        req = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        logging.warning("".join(["\t[HTTP ERROR] ", e.msg]))
        return ""
    logging.info("\treading web page...")
    html = req.read()
    return html


def fetch_url_list(content, pattern_string):
    hrefs = _get_re_list(content, pattern_string)
    res = []
    for url in hrefs:
        res.append(url[6:-1])
    return res


def fetch_month_detail(url="http://www.tianqihoubao.com/lishi/beijing/month/201602.html"):
    '''
     获得对应链接中详细的天气数据
    :param url:
    :return:
    '''
    content = fetch_html(url)
    return _get_re_list(content,
                        """<tr>\s*<td>\s*<a href=[^<]+</a>\s*</td>\s*<td>[^<]+</td>\s*<td>[^<]+</td>\s*<td>[^<]+</td>\s*</tr>""")


def fetch_aqi_month_detail(url="http://www.tianqihoubao.com/aqi/beijing-201602.html"):
    '''

    :param url:
    :return:
    '''
    content = fetch_html(url)

    return _get_re_list(content,
                        """<tr>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<!--\s*<td[^<]+</td>\s*<td[^<]+</td>\s*<td[^<]+</td>\s*\s*-->""")


# main task one
def fetch_lishi_task():
    '''
    fetch lishi
    :return:
    '''
    content = fetch_html(BaseSite + "lishi/")
    url_list = fetch_url_list(content, """href="/lishi/[a-zA-Z0-9]{3,30}\.html\"""")
    total = len(url_list)
    cnt = 0
    for url in url_list:
        key_name = _get_last_key_name(url)
        content = fetch_html(BaseSite + url)
        sub_urls = fetch_url_list(content, """href='/lishi/%s/month/[0-9]{6}\.html'""" % key_name)
        if not os.path.isdir("lishi_" + key_name):
            os.mkdir("lishi_" + key_name)
        print "[WH] processing %s >>>>>>>>( %d / %d )" % (key_name, cnt, total)
        for sub_url in sub_urls:
            detail_list = fetch_month_detail(BaseSite + sub_url)
            sub_key_name = _get_last_key_name(sub_url)
            print "[WH] writing %s(%d)" % (sub_key_name, len(detail_list))
            with open("lishi_" + key_name + "/" + sub_key_name, "w") as ft:
                ft.write((("-" * 30) + "\n\n").join(detail_list))
            print "[WH]", "<" * 15
        print "[WH] ", "<" * 30
        cnt += 1


# main task two
def fetch_aqi_task():
    '''

    :return:
    '''
    content = fetch_html(BaseSite + "aqi/")
    url_list = fetch_url_list(content, """href="/aqi/[a-zA-Z0-9]{3,30}\.html\"""")
    total = len(url_list)
    cnt = 0
    for url in url_list:
        key_name = _get_last_key_name(url)
        content = fetch_html(BaseSite + url)
        sub_urls = fetch_url_list(content, """href='/aqi/%s-[0-9]{6}\.html'""" % key_name)
        if not os.path.isdir("aqi_" + key_name):
            os.mkdir("aqi_" + key_name)
        print "[AQI] processing %s >>>>>>>>( %d / %d )" % (key_name, cnt, total)
        for sub_url in sub_urls:
            detail_list = fetch_aqi_month_detail(BaseSite + sub_url)
            sub_key_name = _get_last_key_name(sub_url)
            print "[AQI] writing %s(%d)" % (sub_key_name, len(detail_list))
            with open("aqi_" + key_name + "/" + sub_key_name, "w") as ft:
                ft.write((("-" * 30) + "\n\n").join(detail_list))
            print "[AQI]", "<" * 15
        print "[AQI]", "<" * 30
        cnt += 1


if __name__ == "__main__":
    fetch_aqi_task()
