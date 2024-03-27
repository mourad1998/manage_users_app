from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseServerError
from rest_framework.parsers import JSONParser
from app_users.models import Profile, User
from app_users.serializers import ProfileSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from rest_framework.request import Request
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def profileApi(request: Request, profile_id=None):
    if request.method == 'GET':
        try:
            # Fetch all profiles
            profiles = Profile.objects.all()
            # Serialize profiles data
            profiles_serializer = ProfileSerializer(profiles, many=True)

            return JsonResponse(profiles_serializer.data, safe=False)
        except Exception as e:
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'POST':
        try:
            # Parse request data
            profile_data = JSONParser().parse(request)
            # Serialize and validate profile data
            profiles_serializer = ProfileSerializer(data=profile_data)
            
            if profiles_serializer.is_valid():
                profiles_serializer.save()
                return JsonResponse({"message": "Profile added successfully"}, status=201)
            
            # Return validation errors if data is invalid
            return JsonResponse(profiles_serializer.errors, status=400)
        except Exception as e:
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'PUT':
        try:
            # Fetch profile object by ID
            profile = Profile.objects.get(id=profile_id)
            # Parse request data
            profile_data = JSONParser().parse(request)
            # Serialize and validate updated profile data
            profiles_serializer = ProfileSerializer(profile, data=profile_data)
            
            if profiles_serializer.is_valid():
                profiles_serializer.save()
                # Return success message
                return JsonResponse({"message": "Profile updated successfully"})
            
            # Return validation errors if data is invalid
            return JsonResponse(profiles_serializer.errors, status=400)
        except ObjectDoesNotExist:
            # Return 404 error if profile does not exist
            return JsonResponse({"error": "Profile not found"}, status=404)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'DELETE':
        try:
            # Delete profile object by ID
            profile = get_object_or_404(Profile, id=profile_id)
            profile.delete()
            # Return success message
            return JsonResponse({"message": "Profile deleted successfully"}, status=204)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)


@csrf_exempt
def userApi(request: Request, user_id=None):
    if request.method == 'GET':
        try:
            # Fetch all users
            user_list = User.objects.all()
            
            # Filter users based on query parameters (username, age, hometown)
            username = request.GET.get('username')
            age = request.GET.get('age')
            hometown = request.GET.get('hometown')
            if username:
                user_list = user_list.filter(username__icontains=username)
            if age:
                user_list = user_list.filter(profile__age=age)
            if hometown:
                user_list = user_list.filter(profile__hometown__icontains=hometown)
                
            # Paginate the filtered user list
            paginator = Paginator(user_list, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            
            # Serialize paginated user data
            users_serializer = UserSerializer(page_obj.object_list, many=True)
            
            # Construct response data with pagination details
            response_data = {
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': page_obj.number,
                'data': users_serializer.data
            }
            
            # Return JSON response with paginated user data
            return JsonResponse(response_data)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'POST':
        try:
            # Parse request data
            user_data = JSONParser().parse(request)
            
            # Serialize and validate user data
            users_serializer = UserSerializer(data=user_data)
            
            if users_serializer.is_valid():
                users_serializer.save()
                return JsonResponse({"message": "User added successfully"}, status=201)
            
            # Return validation errors if data is invalid
            return JsonResponse(users_serializer.errors, status=400)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'PUT':
        try:
            # Fetch user object by ID
            user = User.objects.get(id=user_id)
            # Parse request data
            user_data = JSONParser().parse(request)
            
            # Serialize and validate updated user data
            users_serializer = UserSerializer(user, data=user_data)
            
            if users_serializer.is_valid():
                users_serializer.save()
                return JsonResponse({"message": "User updated successfully"})
            # Return validation errors if data is invalid
            return JsonResponse(users_serializer.errors, status=400)
        except ObjectDoesNotExist:
            # Return 404 error if user does not exist
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)

    elif request.method == 'DELETE':
        try:
            # Delete user object by ID
            user = get_object_or_404(User, id=user_id)
            user.delete()
            # Return success message
            return JsonResponse({"message": "User deleted successfully"}, status=204)
        except Exception as e:
            # Return 500 error if an exception occurs
            return HttpResponseServerError(str(e), status=500)


def profileByUsernameApi(request):
    if request.method == 'GET':
        # Retrieve username from query parameters
        username = request.GET.get('username')
        if username:
            try:
                # Fetch profile object by username
                profile = Profile.objects.get(user__username=username)
                
                # Serialize profile data
                profile_serializer = ProfileSerializer(profile)
                
                # Return JSON response with profile data
                return JsonResponse(profile_serializer.data)
            except Profile.DoesNotExist:
                # Return 404 error if profile does not exist
                return JsonResponse({"error": "Profile not found"}, status=404)
        else:
            # Return 400 error if username parameter is missing
            return JsonResponse({"error": "Username parameter is required"}, status=400)
   
