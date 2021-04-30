from rest_framework import viewsets
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ConvertCurrView(APIView):
    def get(self, request):
        try:
            amount = request.query_params.get("amount", 0)
            curr = request.query_params.get("curr", None)
            to = request.query_params.get("to", None)
            params = {"amount" : amount, "from" : curr, "to": to}
            # import pdb; pdb.set_trace()
            response = requests.get('http://api.frankfurter.app/latest', params=params)
            _data = response.json()
            # lst = to.split(',')
            # msg = "your " + str(amount) + " " + curr + " will be "
            # for target_cur in lst:
            #     msg += str(_data["rates"][target_cur]) + " in " + target_cur
            #     if(lst[-1] != target_cur):
            #         msg += ", "
            # msg += " on " +  _data["date"]
            data = []
            for i in _data['rates']:
                data.append({i : _data['rates'][i]})

            return Response({
                'status': True,
                'message': 'convertion done',
                'data': data
            })
        except Exception:
            return Response({
                'status': False,
                'message': 'Invalid Currency, Please Check',
                'data': []
            })
        


