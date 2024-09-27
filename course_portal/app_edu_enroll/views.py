from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app_edu_enroll.models import Student, Teacher, Course
from app_edu_enroll.serializers import StudentSerializer, TeacherSerializer, CourseSerializer

from django.shortcuts import get_object_or_404

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination

# Create your views here.
# @csrf_exempt
@api_view(["GET", "POST"])
def get_students(request):

    if request.method == "GET":
        qs = Student.objects.all()
        stu_ser = StudentSerializer(qs, many=True).data
        return JsonResponse(stu_ser, safe=False)
    
    if request.method == "POST":
        data = request.data
        ser = StudentSerializer(data=data)

        if ser.is_valid(raise_exception=True):
            ser.save()
            return JsonResponse(ser.data, safe=False)
        
        else:
            return JsonResponse(ser.errors, safe=False)
        
@api_view(["GET","PUT", "DELETE"])
def students_details(request, pk):

    def get_object(pk):
        try:
            obj = Student.objects.get(id=pk)
            return obj
        except Student.DoesNotExist:
            return JsonResponse({"msg":"Object does not exist"}, safe=False)
        
    if request.method == "GET":
        obj = get_object(pk)
        cs = StudentSerializer(obj)
        return JsonResponse(cs.data, safe=False)

    if request.method == "PUT":
        obj = get_object(pk)
        cs = StudentSerializer(obj, request.data, partial=True)

        if cs.is_valid(raise_exception=True):
            cs.save()
            return JsonResponse(cs.data, safe=False)
        else: return JsonResponse(cs.errors, safe=False)
    
    if request.method=="DELETE":
        obj = get_object(pk)
        obj.delete()
        return JsonResponse({"msg":"Object deleted"}, safe=False)
    
class TeacherView(APIView, PageNumberPagination):
    
    def get(self, request):
        qs = Teacher.objects.all()
        paginated_qs = self.paginate_queryset(qs, request, view=self) #paginate using paginate queryset
        cs = TeacherSerializer(paginated_qs, many=True)
        return self.get_paginated_response(cs.data) #response

    def post(self, request):
        data = request.data
        cs = TeacherSerializer(data=data, many=True)
        if cs.is_valid(raise_exception=True):
            cs.save()
            return Response(cs.data, status=status.HTTP_201_CREATED)
        else: return Response(cs.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherViewDeatail(APIView):

    def get(self, request, pk):
        qs = Teacher.objects.get(id=pk)
        cs = TeacherSerializer(qs)
        return Response(cs.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        data = request.data
        qs = Teacher.objects.get(id=pk)
        cs = TeacherSerializer(qs, data=data, partial=True)
        if cs.is_valid(raise_exception=True):
            cs.save()
            return Response(cs.data, status=status.HTTP_200_OK)
        else: return Response(cs.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = Teacher.objects.get(id=pk)

        if obj:
            obj.delete()
            return Response({"msg":"Object Deleted"})
        else: return Response({"msg":"Object not found"}, status=status.HTTP_404_NOT_FOUND)

class CourseView(viewsets.ViewSet):

    def get_queryset(self):
        return Course.objects.all()

    def list(self, request):
        qs = self.get_queryset()
        cs = CourseSerializer(qs, many=True)
        return Response(cs.data, status=status.HTTP_200_OK)

    # def create(self, request):
    #     pass

    # def retrive(self, request, pk):
    #     pass

    # def update(self, request, pk):
    #     pass

    # def destroy(self, request, pk):
    #     pass

class CourseModelView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
