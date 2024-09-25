from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer
from app_edu_enroll.models import Teacher

# class TeacherSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=200)
#     email = serializers.EmailField()

#     class Meta:
#         fields = ['id', 'name', 'email']

#     def create(self, validated_data):
#         return Teacher.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.email = validated_data.get("email", instance.email)
#         instance.save()
#         return instance


class TeacherSerializer(serializers.ModelSerializer):
    email_length = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'name_length', 'email_length']
        extra_kwargs = {'id':{'read_only': True},'name_length':{'read_only': True}}

    def validate(self, name):

        if len(name)<3:
            raise serializers.ValidationError("Name should be morethan 3 characters")
        return name
    
    def get_email_length(self, obj):
        return len(obj.email)






'''
Serializing Data(Update, Retrive)
-------------------
In [24]: Teacher.objects.create(name="Revathi", email="revathi@gmail.com")
Out[24]: <Teacher: Revathi-7>

In [25]: revathi = Teacher.objects.get(id=7)

In [26]: revathi
Out[26]: <Teacher: Revathi-7>

In [27]: TeacherSerializer(revathi)
Out[27]:
TeacherSerializer(<Teacher: Revathi-7>):
    id = IntegerField(read_only=True)
    name = CharField(max_length=200)
    email = EmailField()

In [28]: TeacherSerializer(revathi).data
Out[28]: {'id': 7, 'name': 'Revathi', 'email': 'revathi@gmail.com'}

Deserializing Data(Create)
--------------------
In [29]: new_teacher_data = {"name":"Bharathi", "email":"bharu@gmail.com"}
In [33]: ser_data = TeacherSerializer(data=new_teacher_data)

In [34]: ser_data.is_valid(raise_exception=True)
Out[34]: True

In [35]: ser_data
Out[35]:
TeacherSerializer(data={'name': 'Bharathi', 'email': 'bharu@gmail.com'}):
    id = IntegerField(read_only=True)
    name = CharField(max_length=200)
    email = EmailField()

In [36]: ser_data.save() #obj created in db

Updating data
--------------
In [9]: update_data = {"name":"Revathi Reva"}

In [10]: ser_r = TeacherSerializer(revathi_obj, data=update_data, partial=True)

In [11]: ser_r.is_valid()
Out[11]: True

In [12]: ser_r.save()
Out[12]: <Teacher: Revathi Reva-7>

In [13]: ser_r.data
Out[13]: {'id': 7, 'name': 'Revathi Reva', 'email': 'revathi@gmail.com'}


'''
'''
Why ser.data Doesn't Work When Using data=one_t:
**data** is for deserialization. It expects a //dictionary// or raw input data (like JSON), not a model instance.
**instance** is for serialization. This is where you pass a model instance to be serialized into JSON-like format.
If you try to use data=one_t, the serializer will try to treat one_t as input data, which leads to issues because a model instance isn’t valid raw data.

one_t = Teacher.objects.first()
ser = TeacherSerializer(data=one_t) #wrong
ser = TeacherSerializer(one_t) #right

new_teacher_data = {"name":"Bharathi", "email":"bharu@gmail.com"}
ser_data = TeacherSerializer(data=new_teacher_data) #while deserialization data keyword is must




'''