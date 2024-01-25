import logging
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework import generics
from django.shortcuts import render
from core.views import PaginationClass
from apis.teachers.models import Teacher
from apis.students.models import Student
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apis.users.models import User, AnonymousUser
from rest_framework.pagination import PageNumberPagination


logger = logging.getLogger("myLogger")



# Create your views here.
@api_view(['POST'])
def create_group(request, course_id):
    user = request.user
    try:
        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(user=user)
    except Course.DoesNotExist:
        logger.error( "Course Not Found.", extra={ 'user': user.id })
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except Teacher.DoesNotExist:
        logger.error( "Teacher Not Found.", extra={ 'user': user.id })
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print(course.tutors.all())

    if not request.user.is_a_teacher or teacher not in course.tutors.all():
        logger.error( "You are not authorized to create a group for this course.", extra={ 'user': user.id })
        return Response({'error': 'You are not authorized to create a group for this course'}, status=status.HTTP_403_FORBIDDEN)

    num = ChatGroup.objects.filter(name=request.data.get('name')).count()
    if num > 0:
        logger.warning( "A group with this name already exists.", extra={'user': 'anonymous'} )
        return Response( {"error": "A group with this name already exists."}, status=status.HTTP_409_CONFLICT )
        
    serializer = ChatGroupSerializer(data={'course': course.id, 'name': request.data.get('name')})
    if serializer.is_valid():
        group = serializer.save()

        # Add the teacher to the group members
        group.members.add(user)
        group.save()
        
        logger.error( "Group created successfully.", extra={ 'user': user.id })
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.error( serializer.errors, extra={ 'user': user.id })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def join_group(request):
    user = request.user
    
    if not user.is_authenticated:
        logger.error( "You must provide valid authentication credentials.", extra={ 'user': request.user.id})
        return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # Get code from request body
    code = request.data.get('code', None)
    
    if not code:
        logger.error( "Group code is required in the request body.", extra={ 'user': request.user.id})
        return Response({'error': 'Group code is required in the request body'}, status=status.HTTP_400_BAD_REQUEST)

    # Get group from code 
    try:
        group = ChatGroup.objects.get(code=code)
    except ChatGroup.DoesNotExist:
        logger.error( "Group Not Found.", extra={ 'user': request.user.id})
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if user making request is a student
    if not request.user.is_a_student:
        logger.error( "Only students can join groups.", extra={ 'user': request.user.id})
        return Response({'error': 'Only students can join groups'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if student is registered for the course in question
    try:
        student = Student.objects.get(user=request.user, is_deleted=False)
    except Student.DoesNotExist:
        logger.error( "Student Not found or deleted.", extra={ 'user': request.user.id})
        return Response({'error': 'Student not found or deleted'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the student is registered for the corresponding course
    if group.course not in student.registered_courses.all():
        logger.error( "You are not registered for this course.", extra={ 'user': request.user.id})
        return Response({'error': 'You are not registered for this course'}, status=status.HTTP_403_FORBIDDEN)

    # Check if student is already member of group
    if user in group.members.all():
        logger.error( "You are already a member of this group.", extra={ 'user': request.user.id})
        return Response({'error': 'You are already a member of this group.'}, status=status.HTTP_403_FORBIDDEN)

    # Update the group members
    group.members.add(user)
    group.save()

    serializer = ChatGroupSerializer(group)
    logger.error( "Student joined group {group.name}.", extra={ 'user': request.user.id})
    return Response(serializer.data, status=status.HTTP_200_OK)


 
@api_view(['POST'])
def send_message(request, group_id, *args, **kwargs):
    user = request.user
    
    if not user.is_authenticated:
        logger.error( "You must provide valid authentication credentials.", extra={ 'user': request.user.id})
        return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        chat_group = ChatGroup.objects.get(id=group_id)
    except ChatGroup.DoesNotExist:
        logger.error( "Chat group not found.", extra={ 'user': request.user.id})
        return Response({'error': 'Chat group not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        course = Course.objects.get(id=chat_group.course.id)
    except Course.DoesNotExist:
        logger.error( "Course not found.", extra={ 'user': request.user.id})
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is a student and is registered for the course
    if user.is_a_student:
        try:
            student = Student.objects.get(user=request.user, is_deleted=False)
            if course not in student.registered_courses.all():
                logger.error( "You are not registered for this course.", extra={ 'user': request.user.id } )
                return Response({'error': 'You are not registered for this course'}, status=status.HTTP_403_FORBIDDEN)
        
            # Check if the student has joined the group
            print(chat_group.members.all())
            if user not in chat_group.members.all():
                logger.error("You have not joined the group.", extra={'user': request.user.id})
                return Response({'error': 'You have not joined the group.'}, status=status.HTTP_403_FORBIDDEN)

        except Student.DoesNotExist:
            logger.error( "Student does not exist.", extra={ 'user': request.user.id })    
            return Response({'error': 'Student does not exist'}, status=status.HTTP_403_FORBIDDEN)

    # Check if the authenticated user is a teacher and is assigned to the course
    elif user.is_a_teacher:
        print(course.tutors.all())
        try:
            teacher = Teacher.objects.get(user=request.user, is_deleted=False)
            if teacher not in course.tutors.all():
                logger.warning( "You are not a lecturer of this course", extra={ 'user': request.user.id } )
                return Response( {"error": "You are not a lecturer of this course."}, status.HTTP_403_FORBIDDEN )
        
        except Teacher.DoesNotExist:
            logger.error( "Teacher Does not exist.", extra={ 'user': request.user.id })    
            return Response({'error': 'Teacher Does Not Exist'}, status=status.HTTP_403_FORBIDDEN)
    
    else:
        logger.warning( "Invalid user type", extra={ 'user': request.user.id } )
        return Response({'error': 'Invalid user type'}, status=status.HTTP_403_FORBIDDEN)
    
    
    # Create the message
    data = {
        'content': request.data.get('content', ''),
        'group': chat_group.id,  
        'attachment': request.data.get('attachment', None),  
        'response_to': request.data.get('response_to', None),  
    }

    serializer = GroupMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save(sender=user)
        logger.info( "Message sent successfully", extra={ 'user': request.user.id } )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.warning( serializer.errors, extra={ 'user': request.user.id })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MessagePagination(PageNumberPagination):
    page_size = 30  
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class MessageListAPIView(generics.ListAPIView):
    serializer_class = GroupMessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        group_id = self.kwargs['group_id']  
        try:
            group = ChatGroup.objects.get(id=group_id)
            messages = GroupMessage.objects.filter(group=group).order_by('-timestamp')
            return messages
        except ChatGroup.DoesNotExist:
            logger.error("Group not found.", extra={'user': self.request.user.id})
            return GroupMessage.objects.none()  # Return an empty queryset if the group doesn't exist

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving message list: {str(e)}", extra={'user': request.user.id})
            return Response({'error': 'An error occurred while retrieving messages.'}, status=500)



@api_view(['POST'])
def send_direct_message(request, receiver_id):
    user = request.user
    
    # Check authentication
    if not user.is_authenticated:
        logger.error("You must provide valid authentication credentials.", extra={'user': 'Anonymous'})
        return Response({"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Check if the user is an admin or tutor
    if not user.is_admin and not user.is_a_teacher:
        logger.warning("You are not authorized to send direct messages.", extra={'user': user.id})
        return Response({"error": "You are not authorized to send direct messages."}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve the receiver user object
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        logger.error("Receiver user not found.", extra={'user': user.id})
        return Response({'error': 'Receiver user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if the receiver is an admin or tutor
    if not receiver.is_admin and not receiver.is_a_teacher:
        logger.warning("You can only send direct messages to admins or tutors.", extra={'user': user.id})
        return Response({"error": "You can only send direct messages to admins or tutors."}, status=status.HTTP_403_FORBIDDEN)

    if user == receiver:
        logger.warning("Cannot send a message to yourself.", extra={'user': user.id})
        return Response({'error': 'Cannot send a message to yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create the direct message
    data = {
        'sender': user.id,
        'receiver': receiver_id,
        'content': request.data.get('content', ''),
        'attachment': request.data.get('attachment', None)
    }
    
    serializer = DirectMessageSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Direct message sent to {receiver.username} successfully", extra={'user': user.id})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.warning(serializer.errors, extra={'user': user.id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_user_messages(request, user_id):
    user = request.user

    # Check authentication
    if not user.is_authenticated:
        logger.error("You must provide valid authentication credentials.", extra={'user': 'Anonymous'})
        return Response({"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # Retrieve the other user
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error("User not found.", extra={'user': user.id})
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user can view messages with the other user
    if not user.is_admin and not user.is_a_teacher:
        logger.warning("You are not authorized to view messages with this user.", extra={'user': user.id})
        return Response({"error": "You are not authorized to view messages with this user."}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve messages between the authenticated user and the other user
    messages = DirectMessage.objects.filter(
        Q(sender=user, receiver=other_user) | 
        Q(sender=other_user, receiver=user)
    ).order_by('-timestamp')

    # Serialize the messages
    serializer = DirectMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def inbox_messages(request):
    user = request.user
    
    # Check authentication
    if not user.is_authenticated:
        logger.error("You must provide valid authentication credentials.", extra={'user': 'Anonymous'})
        return Response({"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)


    # Check if the user is an admin or tutor
    if not user.is_admin and not user.is_a_teacher:
        logger.warning("You are not authorized to view inbox messages.", extra={'user': user.id})
        return Response({"error": "You are not authorized to view inbox messages."}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve inbox messages for the user, including both sent and received messages, ordering by the latest first
    inbox_messages = DirectMessage.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-timestamp')

    # Serialize the inbox messages
    serializer = DirectMessageSerializer(inbox_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tutor_group_search(request):
    user = request.user

    if not user.is_authenticated:
        logger.error( "You must provide valid authentication credentials.", extra={ 'user': 'Anonymous' } )
        return Response( {'error': "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED )
    
    if not user.is_a_teacher:
        logger.error( "Only tutors can make this request.", extra={ 'user': 'Anonymous' } )
        return Response( {'error': "Only tutors can make this request."}, status=status.HTTP_401_UNAUTHORIZED )

    try:
        tutor = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        logger.warning( "Tutor Not Found", extra={ 'user': request.user.id } )
        return Response({'error': 'Tutor Not Found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get groups created by the tutor
    created_groups = ChatGroup.objects.filter(course__tutors=tutor)

    # Filter groups based on any additional search parameters if needed
    keyword = request.query_params.get('keyword', None)

    if keyword is not None:
        # Split the keyword into individual words
        words = keyword.split()

        # Create a Q object for each word in both fields
        name_queries = Q()

        for word in words: 
            name_queries |= Q(name__icontains=word)

        # Apply the query along with other filters
        created_groups = created_groups.filter(name_queries).order_by('-created_at')
        
    # Paginate the results
    paginator = PaginationClass()
    paginated_groups = paginator.paginate_queryset(created_groups, request)

    # Serialize the groups
    group_serializer = ChatGroupSerializer(paginated_groups, many=True)

    # Create the response
    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'groups': group_serializer.data,
    }

    return Response(response_data)


# class MyInbox(generics.ListAPIView):
#     pass


