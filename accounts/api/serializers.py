from rest_framework import serializers
from accounts.models import User,BranchAdmin,Branch,Course,Subject,Topic,Batch,Module,SubTopic

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile','password']
        # fileds = '__all__'


    def get_name(self,obj):
        name=obj.username
        return name
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']




class BranchAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchAdmin
        fields = '__all__'
        # fields = ['email','password','superadmin']

# class BranchAdminLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BranchAdmin
#         # exclude = ('superadmin','branch')
#         fields = ['email', 'password' ]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name', 'location']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        # depth =1
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
        # depth = 1
class SubjectSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'
    def get_course_name(self, obj):
        return obj.course.name

class ModuleSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    class Meta:
        model = Module
        fields = '__all__'
    def get_subject_name(self, obj):
        return obj.subject.name
    def get_course_name(self, obj):
        return obj.subject.course.name

class TopicSerializer(serializers.ModelSerializer):
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    class Meta:
        model = Topic
        fields = '__all__'
    def get_module_name(self, obj):
        return obj.module.name
    def get_subject_name(self, obj):
        return obj.module.subject.name
    def get_course_name(self, obj):
        return obj.module.subject.course.name

class SubTopicSerializer(serializers.ModelSerializer):
    topic_name = serializers.SerializerMethodField()
    module_name = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = SubTopic
        # fields = '__all__'
        fields = ['id', 'name', 'topic_name', 'module_name', 'subject_name', 'course_name']
    def get_topic_name(self, obj):
        return obj.topic.name
    def get_module_name(self, obj):
        return obj.topic.module.name
    def get_subject_name(self, obj):
        return obj.topic.module.subject.name
    def get_course_name(self, obj):
        return obj.topic.module.subject.course.name