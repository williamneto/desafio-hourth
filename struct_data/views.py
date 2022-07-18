import requests
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

SOURCE_API = "https://mc3nt37jj5.execute-api.sa-east-1.amazonaws.com/default/hourth_desafio"

def proccess_data(data, start_date, finish_date):
    filtered = []

    if start_date and finish_date:
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
            if item_datetime >= start_datetime and item_datetime <= finish_datetime:
                filtered.append(item)
    else:
        filtered = data

    result_dict = {}
    for item in filtered:
        if not item["product_url"] in result_dict:
            product_dict = {
                "product_url__image": item["product_url__image"],
                "product_url": item["product_url"],
                "product_url__created_at": item["product_url__created_at"],
                "total_sales": item["vendas_no_dia"],
                item["consult_date"]: item["vendas_no_dia"]
            }

            result_dict[item["product_url"]] = product_dict
        else:
            result_dict[item["product_url"]]["total_sales"] += item["vendas_no_dia"]
            result_dict[item["product_url"]][item["consult_date"]] = item["vendas_no_dia"]
    
    final = []
    for item in result_dict:
        item_dict = result_dict[item]

        if not start_date or not finish_date:
            final.append(item_dict)
            print(final)
        else:
            finish_datetime = datetime(
                int(finish_date.split("-")[0]),
                int(finish_date.split("-")[1]),
                int(finish_date.split("-")[2])
            )
            date_to_verify = datetime(
                int(start_date.split("-")[0]),
                int(start_date.split("-")[1]),
                int(start_date.split("-")[2])
            )


            while True:
                date_to_verify_str = "%s-%s-%s" % (
                    str(date_to_verify.year),
                    str(date_to_verify.month).zfill(2),
                    str(date_to_verify.day).zfill(2)
                )
                
                if not date_to_verify_str in item_dict:
                    item_dict[date_to_verify_str] = 0
                
                if not item_dict in final:
                    final.append(item_dict)
                
                if date_to_verify == finish_datetime:
                    break

                date_to_verify = date_to_verify + timedelta(days=1)

    return final

# Percorrer todas as vendas
# Agrupar itens com o mesmo product_url
# Tornar os valores consult_date em chaves dentro do json
# Somar os valores da coluna vendas_no_dia de cada um dos 
# dias e atribuir esse valor somado à chave total_sales
def api(request):
    response = requests.get(SOURCE_API)
    data = response.json()
    start_date = request.GET.get("start_date")
    finish_date = request.GET.get("finish_date")

    
    return JsonResponse(
        proccess_data(data, start_date, finish_date),
        safe=False
    )

    return JsonResponse(filtered, safe=False)
    