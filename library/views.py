from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Admin, Book
from .serializers import AdminLoginSerializer, AdminSignupSerializer, BookSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class AdminSignupAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            admin = serializer.save()
            token, created = Token.objects.get_or_create(user=admin)

            return Response({
                'token': token.key,
                'admin_id': admin.id,
                'email': admin.email,
            }, status=status.HTTP_201_CREATED)

        except Exception as err:
            return Response(
                {'error': str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminLoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if not user:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user.last_login = timezone.now()
            user.save()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'admin_id': user.id,
                'email': user.email,
            }, status=status.HTTP_200_OK)

        except Exception as err:
            return Response(
                {'error': str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request)
        try:
            request.user.auth_token.delete()
            return Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_200_OK
            )
        except Exception as err:
            return Response(
                {'error': str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def books_api(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
        return Response(
            {'error': str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book_api(request):
    serializer = BookSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response(
            {'error': 'Book with this ISBN already exists'},
            status=status.HTTP_409_CONFLICT
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        return Response({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publication_year': book.publication_year,
            'available': book.available
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book_api(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except IntegrityError:
        return Response(
            {'error': 'Book with this ISBN already exists'},
            status=status.HTTP_409_CONFLICT
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_api(request, pk):
    try:
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(
            {'message': 'Book deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def student_view(request):
    books = Book.objects.all()
    return render(request, 'library/student_view.html', {'books': books})
