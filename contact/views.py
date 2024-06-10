from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from contact.models import Contact
from account.mixins import NormalUserPermissionMixin


# Create your views here.
class ContactView(NormalUserPermissionMixin ,APIView):

    class ContactSerailizers(serializers.ModelSerializer):
        class Meta:
            model=Contact
            fields='__all__'

    def post(self,request):
        data=request.data
        serializer = self.ContactSerailizers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
