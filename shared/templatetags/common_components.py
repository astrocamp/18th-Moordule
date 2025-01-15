from django import template

register = template.Library()


@register.inclusion_tag("shared/moordule_button.html")
def moordule_button(*, text, color):
    return {"text": text, "color": color}


@register.inclusion_tag("shared/icon.html")
def icon(*, name):
    return {"name": name}


@register.inclusion_tag("shared/meetup_recommended_card.html")
def meetup_recommended_card(meetup=None):
    if meetup is None:
        meetup = {}
    return {"meetup": meetup}


@register.inclusion_tag("shared/accordion.html")
def accordion():
    items = [
        {
            "id": "a1",
            "label": "歡迎來到 Moordule多揪！",
            "content": "感謝您選擇 Moordule 多揪！與傳統的一對一交友平台不同，我們以聚會為起點，讓用戶在實際互動中建立更真實的連結。這裡，您可以與志同道合的人共同參與活動、交流，享受更多元且豐富的交友體驗。",
        },
        {
            "id": "a2",
            "label": "如何註冊 Moordule 多揪 帳號？",
            "content": "註冊 Moordule 多揪 帳號非常簡單。只需設定Email及密碼，並按照指示完成註冊過程，即可開啟您的專屬帳號。完成註冊後，您即可進入帳號頁面，完整個人資訊後，便能開始使用平台的所有功能，與其他用戶互動、創建或參加聚會等。",
        },
        {
            "id": "a3",
            "label": "如何參加聚會？",
            "content": "在 Moordule 多揪 平台上，當您註冊並登入後，即可開始參加各種聚會活動。提醒您，請務必遵守平台守則，避免任何違規行為，這樣您就能愉快地與志同道合的人一起交流並參加聚會。",
        },
        {
            "id": "a4",
            "label": "創建聚會後，我是否可以取消或修改我的活動？",
            "content": "在 Moordule 多揪，當您創建一個聚會後，請仔細確認活動的詳細資料。若活動尚未開始，您可修改或取消活動。如果您決定取消已創建的活動，平台將根據相關規定進行處理，並可能影響您的帳號或點數。請詳讀平台的創建規則與扣款規則，了解更多有關取消活動的資訊。",
        },
        {
            "id": "a5",
            "label": "Moordule 多揪 是否會保護我的個人資訊？",
            "content": "是的，您的隱私對我們來說至關重要。Moordule 多揪 嚴格遵守隱私政策，並采取各種措施保護您的個人資料不受外界侵害。詳細的隱私政策內容，您可以在網站上查看或隨時聯繫客服詢問。",
        },
        {
            "id": "a6",
            "label": "如何聯繫客服？",
            "content": "若您有任何問題或需要協助，您可以透過電子郵件聯繫我們。我們將儘快回覆您的問題並提供解答。",
        },
    ]
    return {"items": items}
