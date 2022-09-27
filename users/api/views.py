from .serializers import AccountSerializer 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
# from users import models 


@api_view(["POST"])
def create_account(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        account_details = serializer.save()
        serializer_data = serializer.data
        refresh = RefreshToken.for_user(account_details)
        serializer_data["token"] = {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                   }
        return Response(serializer_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        msg = "Successfully logged out"
        return Response(msg, status=status.HTTP_200_OK)
    
        
             
        