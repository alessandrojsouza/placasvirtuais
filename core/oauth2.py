
import json
import requests

from django.http import HttpResponse


class OAuth2Response(HttpResponse):
    def __init__(self, request):
        REDIRECT_URI = 'http://localhost:8000/suap_login/'
        CLIENTE_ID = ''
        CLIENT_SECRET = ''
        AUTHORIZE_URL = 'https://suap.ifrn.edu.br/o/authorize/'
        ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
        USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'
        authorize_url = '{}?response_type=code&client_id={}&redirect_uri={}'.format(
            AUTHORIZE_URL, CLIENTE_ID, REDIRECT_URI
        )
        access_token_request_data = dict(
            grant_type='authorization_code',
            code=request.GET.get('code'),
            redirect_uri=REDIRECT_URI,
            client_id=CLIENTE_ID,
            client_secret=CLIENT_SECRET
        )
        if 'code' in request.GET:
            html = ''
            data = json.loads(requests.post(ACCESS_TOKEN_URL, data=access_token_request_data, verify=False).text)
            headers = {'Authorization': 'Bearer {}'.format(data.get('access_token')), 'x-api-key': CLIENT_SECRET}
            self.data = json.loads(requests.get(USER_DATA_URL, data={'scope': data.get('scope')}, headers=headers).text)
        else:
            self.data = None
            html = '<html><script>document.location.href="{}";</script></html>'
        super().__init__(html.format(authorize_url))
