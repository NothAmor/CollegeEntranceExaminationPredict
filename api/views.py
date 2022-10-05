from genericpath import isfile
from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
from . import models

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent

def spider(request):
    if request.method == "POST":
        url = "http://www.creditsailing.com"
        year = int(request.POST.get("year"))
        province = request.POST.get("province")

        # 如果已有文件，删除
        filename = os.path.join(BASE_DIR, 'static', 'csv', "{year}_{province}.csv".format(year=year, province=province))
        if Path(filename).exists():
            os.remove(filename)

        if year == 2022:
            rankingUrl = "http://www.creditsailing.com/school/yfyd/11/2022/3/2691352.html"
            response = requests.get(rankingUrl)
            response.encoding = "GBK"
            soup = BeautifulSoup(response.text, "html.parser")

            locationList = soup.find_all(name="a", attrs={"class": "sch-cell"})[:-5]

            status = False
            for location in locationList:
                if province == re.sub('[^\u4e00-\u9fa5]+','', str(location.string)):
                    status = True
                    provinceUrl = url + location["href"]
                    break
            
            if status:
                pass
            else:
                return HttpResponse("爬取错误, 未找到对应省份, 省份是{province}".format(province=province))

            df = pd.read_html(provinceUrl)
            data = pd.concat(df)
            #data.drop(0, inplace=True)
            data.to_csv(os.path.join(BASE_DIR, 'static', 'csv', "{year}_{province}.csv".format(year=year, province=province)), index=None, encoding="utf-8")
            #models.FenDuan.objects.create()

            return HttpResponse("爬取成功")
        else:
            # 先随便爬一个页面
            rankingUrl = "http://www.creditsailing.com/school/yfyd/11/2022/3/2691352.html"
            response = requests.get(rankingUrl)
            response.encoding = "GBK"
            soup = BeautifulSoup(response.text, "html.parser")

            # 拿到所有需要用的a标签
            locationList = soup.find_all(name="a", attrs={"class": "sch-cell"})

            rightUrl = ""

            # 开始遍历
            status = False
            for location in locationList:
                # 寻找到要找的省份
                if province == re.sub('[^\u4e00-\u9fa5^0-9]', '', str(location.string)):
                    status = True
                    provinceUrl = url + location["href"]

                    # 请求这个省份，去拿这个省份对应年份的数据
                    response = requests.get(provinceUrl)
                    response.encoding = "GBK"

                    soup = BeautifulSoup(response.text, "html.parser")
                    tempList = soup.find_all(name="a", attrs={"class": "sch-cell"})
                    # 遍历所有地区
                    for temp in tempList[-10:]:
                        # 拿到对应的年份URL
                        if str(year) in str(temp.string):
                            rightUrl = url + temp['href']
                            break
                if status:
                    break

            if status:
                pass
            else:
                return HttpResponse("爬取错误, 未找到对应省份, 省份是{province}".format(province=province))

            tempdf = pd.read_html(rightUrl)
            data = pd.concat(tempdf)
            data.to_csv(os.path.join(BASE_DIR, 'static', 'csv', "{year}_{province}.csv".format(year=year, province=province)), index=None, encoding="utf-8")
            return HttpResponse("爬取成功")


def preview(request):
    return HttpResponse("test")