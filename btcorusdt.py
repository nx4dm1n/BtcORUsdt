#coding:utf-8
#author:her0m[at]qq[dot]com
#获取BTC、USDT市场均价及火币c2c交易区的出售均价；
#计算固定本金情况下，两个币的人民币差价，得出购买那种币较划算；


import sys
import requests
from pyquery import PyQuery
import json
import urllib
import re

#获取比特币的市场均价，参考了7个交易所的市场价
def GetBtcMarketPrice():
    list1=['1','2','3','4','5','6','7']
    pricelist=[]

    #marketRes=requests.get("http://www.feixiaohao.com/currencies/bitcoin/")
    marketRes=PyQuery(url="http://www.feixiaohao.com/currencies/bitcoin/")
    #xxx=marketRes("#markets").html()
    for data in marketRes("tr"):
        priceinfo=PyQuery(data).text().encode("utf-8")
        if priceinfo[0] in list1:
            prices=priceinfo.split(" ")[3].replace("¥","")
            prices=prices.replace(",","")
            pricelist.append(int(prices))

    return sum(pricelist)/len(pricelist)

def GetUSDTmarketPrice():
    '''
    url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
    req = requests.get(url)
    html = req.text
    #print(html)
    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)


    USDTmarketPrice = float(sjson["Data"][0][0][1]/10000.00)
    return USDTmarketPrice
    '''
    list1=['1','2','3','4','5','6','7']
    pricelist=[]

    #marketRes=requests.get("http://www.feixiaohao.com/currencies/bitcoin/")
    marketRes=PyQuery(url="http://www.feixiaohao.com/currencies/tether/")
    #xxx=marketRes("#markets").html()
    for data in marketRes("tr"):
        priceinfo=PyQuery(data).text().encode("utf-8")
        if priceinfo[0] in list1:
            prices=priceinfo.split(" ")[3].replace("¥","")
            prices=prices.replace(",","")
            pricelist.append(float(prices))

    return sum(pricelist)/len(pricelist)

#获取火币c2c交易区，出售比特币的均价
def GetBtcHuoPrice():
    huopricelist = []
    paramslist = {'coinId':'1','tradeType':'1','currentPage':'1','payWay':'','country':''}
    headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    huores = requests.get("https://api-otc.huobi.pro/v1/otc/trade/list/merchant",params = paramslist,headers = headers)
    dictstr = json.loads(huores.text)
    for prices in dictstr['data']:
        huopricelist.append(int(prices['price']))

    return sum(huopricelist)/len(huopricelist)

def GetUSDThuoPrice():
    huopricelist = []
    paramslist = {'coinId':'2','tradeType':'1','currentPage':'1','payWay':'','country':''}
    headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    huores = requests.get("https://api-otc.huobi.pro/v1/otc/trade/list/merchant",params = paramslist,headers = headers)
    dictstr = json.loads(huores.text)
    for prices in dictstr['data']:
        huopricelist.append(prices['price'])

    return sum(huopricelist)/len(huopricelist)

if __name__=="__main__":
    
    USDTmarketPrice = GetUSDTmarketPrice()
    USDThuoPrice = GetUSDThuoPrice()

    BtcMarketPrice = GetBtcMarketPrice()
    BtcHuoPrice = GetBtcHuoPrice()

    rmbYuan = 1000

    print "BTC市场均价：",BtcMarketPrice
    print "BTC火币c2c交易区均价：",BtcHuoPrice

    # BtcNM，1000元人民币按照市场均价可购买的BTC数量；
    # BtcNH，1000元人民币按照huobi.pro c2c交易区的均价可购买的BTC数量
    BtcNM = float(rmbYuan)/float(BtcMarketPrice)
    BtcNH = float(rmbYuan)/float(BtcHuoPrice)

    # rmbLost，按照huobi.pro c2c交易区均价买入1000元人民币的BTC，相比按照市场均价买入损失的人民币金额
    rmbLost = BtcMarketPrice*(BtcNM-BtcNH)
    print "huobi.pro c2c交易区购买1000元的BTC相比市场均价损失的人民币金额：", rmbLost

    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "---------------------------------------------------------------"

    print "USDT市场均价：",USDTmarketPrice
    print "USDT火币c2c交易区均价：",USDThuoPrice

    UsdtNM = float(rmbYuan)/USDTmarketPrice
    UsdtNH = float(rmbYuan)/USDThuoPrice

    rmblost1 = USDTmarketPrice*(UsdtNM-UsdtNH)
    print "huobi.pro c2c交易区购买1000元的USDT相比市场价损失的人民币金额：", rmblost1
