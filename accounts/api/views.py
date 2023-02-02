from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TopicSerializer, ModuleSerializer, UserSerializer,BranchAdminSerializer,BranchSerializer,CourseSerializer,BatchSerializer,SubjectSerializer
from rest_framework import status,generics
from rest_framework.views import APIView
from django.shortcuts import render 
from accounts.models import BranchAdmin,Branch,Course,Batch,Subject,Module,Topic
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password,check_password
from rest_framework import generics, authentication, permissions
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token

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

############# CREATING BRANCH ADMIN #########


class CreateBranchAdmin(generics.CreateAPIView):
    serializer_class = BranchAdminSerializer

    def post(self, request, *args, **kwargs):
        # if not request.user.is_superuser:
        #     return Response({"message": "Only superuser can create a BranchAdmin"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password')
        hash_password = make_password(password)
        print(request.data.get('password'))
        serializer.validated_data['password'] = hash_password

        user = BranchAdmin.objects.create(
            email=serializer.validated_data["email"],
            superadmin=serializer.validated_data["superadmin"],
            branch=serializer.validated_data["branch"],
            password=serializer.validated_data["password"],
        )
        # user.set_password(serializer.validated_data["password"])
        user.save()

        # BranchAdmin.objects.create(
        #     user=user,
        #     branch=serializer.validated_data["branch"]
        # )

        return Response({"message": "BranchAdmin created successfully"}, status=status.HTTP_201_CREATED)


############# CREATING BRANCH ADMIN ENDS #########

#####BranchAdmin Login #########
class BranchAdminLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # if not request.user.is_superuser:
        #     return Response({"message": "Only superuser can create a BranchAdmin"}, status=status.HTTP_403_FORBIDDEN)
        email = request.data['email']
        password = request.data['password']
        
        serializer = BranchAdmin.objects.get(email=email)
        if check_password(password,serializer.password):
            return Response("You are logged in")
        return Response('You are not allowed to log in to this branch')
#####BranchAdmin Login #########


#####BRANCH CREATION #########

class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a Branch"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####BRANCH CREATION ENDS #########

#####BRANCH CRUD OPERATIONS #########

class BranchRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####BRANCH CRUD OPERATIONS ENDS #########


#####COURSE CRUD OPERATIONS  #########

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a course"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####COURSE CRUD OPERATIONS ENDS #########

#####BATCH CRUD OPERATIONS  #########

class BatchCreateView(generics.CreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a Batch"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class BatchRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####BATCH CRUD OPERATIONS ENDS #########


#####SUBJECT CRUD OPERATIONS  #########

class SubjectCreateView(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a Subject"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####SUBJECT CRUD OPERATIONS ENDS #########


#####MODULE CRUD OPERATIONS  #########

class ModuleCreateView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a Module"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class ModuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####MODULE CRUD OPERATIONS ENDS #########

#####TOPIC CRUD OPERATIONS  #########

class TopicCreateView(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can create a Topic"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

class TopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"message": "Only admin can Do Operations"}, status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)

#####TOPIC CRUD OPERATIONS ENDS #########

