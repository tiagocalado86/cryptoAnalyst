from django.shortcuts import render
from django.http import HttpResponse
from services.aiService import AIService
from services.cryptoService import CryptoService
from services.webScrappingService import WebScrappingService
from dotenv import load_dotenv
import os

def index(request):
    return HttpResponse("WELCOME!")

def fetchData(request):
    load_dotenv()

    #url to get crypto data from CMC
    urlCMC = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    headersCMC = {
        "X-CMC_PRO_API_KEY": os.getenv("API_KEY_CMC")
    }
    paramsCMC = {
        'start':'1',
        'limit':'10',
        'convert':'EUR'
    }

    #url to get crypto news from coindesk
    urlNews = "https://www.coindesk.com/latest-crypto-news"

    #usage of services to fetch data
    CryptoService.getCryptoInfo(urlCMC, headersCMC, paramsCMC)
    WebScrappingService.getNews(urlNews)

    return HttpResponse("")

def cryptoAnalyzer(request):

    if request.method == "POST":

        msg = request.POST.get("msg")

        if not msg:
            msg = "Make a market analysis and provide advice for investment based on the following data:"

        return render(request, 'ui.html', {'msg': AIService.getCryptoAnalysis(msg)})
    return render(request, 'ui.html')
