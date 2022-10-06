from django.http import HttpResponse, HttpResponseRedirect
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn import linear_model
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

            return HttpResponseRedirect("/main/spider")
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
            return HttpResponseRedirect("/main/spider")


def predict(request):
    if request.method == "POST":
        # 获取POST变量
        province = request.POST.get("province")
        year = request.POST.get("year")
        grade = request.POST.get("grade")

        # 判断该省份是否存在五年数据
        fileStatus = False
        for i in range(2018, 2023):
            filename = "{year}_{province}.csv".format(year=i, province=province)
            if Path(os.path.join(BASE_DIR, 'static', 'csv', filename)).exists():
                fileStatus = True
                break
        
        # 不存在五年数据，跳出
        if fileStatus == False:
            return HttpResponse("请求失败，请提前爬取该省份5年高考一分一段数据")

        # 开始分析
        xdata = []

        # 读取五年数据
        data1 = pd.read_csv(os.path.join(BASE_DIR, 'static', 'csv', '2022_{province}.csv'.format(province=province)))
        data2 = pd.read_csv(os.path.join(BASE_DIR, 'static', 'csv', '2021_{province}.csv'.format(province=province)))
        data3 = pd.read_csv(os.path.join(BASE_DIR, 'static', 'csv', '2020_{province}.csv'.format(province=province)))
        data4 = pd.read_csv(os.path.join(BASE_DIR, 'static', 'csv', '2019_{province}.csv'.format(province=province)))
        data5 = pd.read_csv(os.path.join(BASE_DIR, 'static', 'csv', '2018_{province}.csv'.format(province=province)))

        # 将五年数据合并到一起
        mergedData = pd.concat([data1, data2, data3, data4, data5])
        # 初始化线性回归预测模型
        lm = linear_model.LinearRegression()
        
        # 预处理分数数据集
        for index, row in mergedData.iterrows():
            xdata.append([row["分数"]])
        
        # 初始化xy轴
        X = xdata
        y = mergedData["建议位次"]
        model = lm.fit(X, y)
        # print(model.intercept_, model.coef_)

        return HttpResponse("预测成功，预测你在{year}年{province}省高考排名位次是{result}".format(year=year, province=province, result=int(model.predict([[int(grade)]])[0])))
    else:
        return HttpResponse("错误请求API方法")