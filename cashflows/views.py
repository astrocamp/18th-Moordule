import base64
import hashlib
import hmac
import json
import uuid

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from moordule import settings
from .models import Payment


def index(request):
    return render(request, "index.html")


# line pay API header
def create_headers(body, uri):
    channel_id = settings.LINE_CHANNEL_ID
    secret_key = settings.LINE_CHANNEL_SECRET_KEY
    nonce = str(uuid.uuid4())  # TODO:確認使用nonc是用uuid?
    # header 轉換成json格式
    body_to_json = json.dumps(body)

    # 組裝簽名
    message = secret_key + uri + body_to_json + nonce

    binary_message = message.encode()
    binary_secret_key = secret_key.encode()

    # 雜湊
    hash = hmac.new(binary_secret_key, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": channel_id,
        "X-LINE-ChannelSecret": secret_key,
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }
    return headers


# line pay API body
@login_required
def request_payment(request):
    if request.method == "POST":
        # 設定訂單與付款資訊
        order_id = f"order_{str(uuid.uuid4())}"
        package_id = f"package_{str(uuid.uuid4())}"
        payload = {
            "amount": 699,
            "currency": "TWD",
            "orderId": order_id,
            "packages": [
                {
                    "id": package_id,
                    "amount": 699,
                    "products": [
                        {
                            "id": "1",
                            "name": "方案Ｂ超好揪",
                            "quantity": 1,
                            "price": 699,
                        }
                    ],
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"https://{settings.HOSTNAME}/cashflows/payment/confirm",
                "cancelUrl": f"https://{settings.HOSTNAME}/payment/cancel",
            },
        }

        # 發送 API 請求
        uri = settings.LINE_REQUEST_URL
        headers = create_headers(payload, uri)
        url = f"{settings.LINE_SANDBOX_URL}{uri}"
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 根據狀態，處理回應
        if response.status_code == 200:
            data = response.json()
            if data["returnCode"] == "0000":
                # 儲存付款資訊至資料庫，並關聯到當前用戶
                Payment.objects.create(
                    user=request.user,  # 將當前用戶儲存到 Payment 中
                    order_id=order_id,
                    transaction_id=data["info"]["transactionId"],  # 假設這裡有交易ID
                    amount="699",
                    currency="TWD",
                    status="待確認"  # 初始狀態可以設為待確認
                )
                return redirect(data["info"]["paymentUrl"]["web"])
            else:
                return render(
                    request, "payment/error.html", {"message": data["returnMessage"]}
                )
        else:
            return render(
                request,
                "payment/error.html",
                {"message": f"Error: {response.status_code}"},
            )

    return render(request, "payment/checkout.html")

def confirm(request):
    return render(request, "payment/confirm.html")
    # transaction_id = request.GET.get('transactionId')  
    # amount = request.GET.get('amount')  
    # currency = request.GET.get('currency')  

    # uri = f"/v3/payments/{transaction_id}/confirm"
    # headers = create_headers({"amount": amount, "currency": currency}, uri)
    # url = f"{settings.LINE_SANDBOX_URL}{uri}"
    
    # response = requests.post(url, headers=headers, data=json.dumps({"amount": amount, "currency": currency}))

    # if response.status_code == 200:
    #     data = response.json()
    #     if data["returnCode"] == "0000":
    #         # 儲存付款資訊至資料庫，並關聯到當前用戶
    #         Payment.objects.create(
    #             user=request.user,
    #             order_id=data["info"]["orderId"],
    #             transaction_id=transaction_id,
    #             amount=amount,
    #             currency=currency,
    #             status='成功'
    #         )
    #         return render(request, "payment/confirm.html", {"data": data})
    #     else:
    #         return render(request, "payment/error.html", {"message": data["returnMessage"]})
    # else:
    #     return render(request, "payment/error.html", {"message": f"Error: {response.status_code}"})
