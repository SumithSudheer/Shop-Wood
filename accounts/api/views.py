from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser
        token['email'] = user.email
        token['is_active'] = user.is_active
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Register(APIView):  
     def post(self,request):
        data = request.data
        # print ("hii",data)
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
                serializer.save()
                # print(serializer.data)
                phone_number=data['mobile']
               
                

                response={
                    "messages" : "User Created Successfully",
                    "data" : serializer.data
                }
                
                return Response(data = response, status = status.HTTP_201_CREATED)
            
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)