def get_referrer_params(request):
    referrers = [
        request.META.get("HTTP_REFERER"),
        *request.GET.getlist("referer"),
        *request.GET.getlist("referrer"),
    ]
    referrers = [r for r in referrers if r]
    get_params = {
        "referrer": ", ".join(referrers),
    }
    for key in request.GET:
        if key.startswith("utm_"):
            value = ", ".join(request.GET.getlist(key))
            get_params[key] = value
    return {
        **get_params,
    }
