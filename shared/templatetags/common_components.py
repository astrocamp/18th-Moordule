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
            "content": "我們希望您能夠在 Moordule多揪 享受聊天交友的樂趣，也能感受到輕鬆和安心的社區氛圍。Moordule多揪 歡迎每一個能夠真誠、友善、懂得尊重他人的人，也歡迎並期待您能夠跟 Moordule多揪 一起建立一個和諧友好的交友平台。Moordule多揪 鼓勵用戶在不冒犯他人的前提下，自由、勇敢地表達和展現自己，收穫更多新鮮有趣的體驗。為了讓所有人有更好交友環境，請閱讀並遵守平台准則。任何違反准則的行為都有可能會導致您被禁止使用Moordule多揪，並永久地失去您的帳號。",
        },
        {
            "id": "a2",
            "label": "如何參加聚會",
            "content": "在 Moordule多揪 平台上，當您註冊並登入之後，便可以參加聚會聚會。貼心小提醒，請確保遵守平台守則，避免違規行為，一起享受和志趣相同的人相聚。",
        },
        {
            "id": "a3",
            "label": "如何聯繫客服？",
            "content": "您可以透過電子郵件與我們聯繫，我們將盡快回覆您的問題。",
        },
    ]
    return {"items": items}
