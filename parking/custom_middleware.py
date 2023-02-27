class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print("Middleware created before view")
        response = self.get_response(request)  
        # print("Middleware created after view")
        # print(request.user)
        return response  
