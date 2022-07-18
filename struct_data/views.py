import requests
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

SOURCE_API = "https://mc3nt37jj5.execute-api.sa-east-1.amazonaws.com/default/hourth_desafio"


# Percorrer todas as vendas
# Agrupar itens com o mesmo product_url
# Tornar os valores consult_date em chaves dentro do json
# Somar os valores da coluna vendas_no_dia de cada um dos 
# dias e atribuir esse valor somado à chave total_sales
def index(request):
    response = requests.get(SOURCE_API)
    data = response.json()
    start_date = request.GET.get("start_date")
    finish_date = request.GET.get("finish_date")

    filtered = []

    if start_date and finish_date:
        print(int(start_date.split("-")[0]))
        start_datetime = datetime(
            int(start_date.split("-")[0]),
            int(start_date.split("-")[1]),
            int(start_date.split("-")[2])
        )
        finish_datetime = datetime(
            int(finish_date.split("-")[0]),
            int(finish_date.split("-")[1]),
            int(finish_date.split("-")[2])
        )

        for item in data:
            item_datetime = datetime(
                int(item["consult_date"].split("-")[0]),
                int(item["consult_date"].split("-")[1]),
                int(item["consult_date"].split("-")[2])
            )
            if item_datetime > start_datetime and item_datetime < finish_datetime:
                filtered.append(item)
    else:
        pass

    return JsonResponse(filtered, safe=False)
    