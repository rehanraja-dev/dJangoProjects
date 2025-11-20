from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from rest_framework import status

# Simulate AI response (for now)
def mock_ai_response(user_message):
    # You can later replace this with OpenAI API or RAG logic
    return f"I received your message: '{user_message}'. This is a mock AI reply."

# Send message to AI
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    user = request.user
    user_message = request.data.get('content')

    if not user_message:
        return Response({'error': 'Message content required'}, status=status.HTTP_400_BAD_REQUEST)

    # Save user's message
    user_msg = Message.objects.create(user=user, role='user', content=user_message)

    # Get AI response
    ai_reply = mock_ai_response(user_message)

    # Save AI's message
    ai_msg = Message.objects.create(user=user, role='ai', content=ai_reply)

    # Return both as response
    return Response({
        'user_message': MessageSerializer(user_msg).data,
        'ai_message': MessageSerializer(ai_msg).data
    }, status=status.HTTP_201_CREATED)


# Get chat history for current user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    messages = Message.objects.filter(user=request.user).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
