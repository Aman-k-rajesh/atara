from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
import json
from .models import Messages_Tb
from service.models import Service_DB
from user.models import com_TB

@login_required
def user_chat(request, service_id=None):
    """User chat view where they can select a service center and chat with them."""
    services = Service_DB.objects.filter(approve=True)  # Fetch only approved service centers

    if service_id:
        selected_service = get_object_or_404(Service_DB, id=service_id)
        messages = Messages_Tb.objects.filter(
            sender_user=request.user.com_tb, receiver_service=selected_service
        ) | Messages_Tb.objects.filter(
            sender_service=selected_service, receiver_user=request.user.com_tb
        )
        messages = messages.order_by("timestamp")  # Sort messages in chronological order
    else:
        selected_service = None
        messages = None

    return render(request, "chat/user_chat.html", {
        "services": services,
        "selected_service": selected_service,
        "messages": messages,
    })

@csrf_exempt
def send_message(request):
    """Handle sending messages from user to service"""
    if request.method == "POST":
        data = json.loads(request.body)
        user = get_object_or_404(com_TB, id=request.session.get("user_id"))
        service = get_object_or_404(Service_DB, id=data["service_id"])

        message = Messages_Tb.objects.create(
            sender_user=user,
            receiver_service=service,
            message=data["message"],
            timestamp=now(),
            is_read=False
        )

        return JsonResponse({"status": "Message sent!", "message_id": message.id})






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Messages_Tb
from user.models import com_TB
from service.models import Service_DB
from django.utils.timezone import now

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Messages_Tb
from user.models import com_TB
from service.models import Service_DB
from django.utils.timezone import now

@csrf_exempt
def save_message(request):
    """Store new chat messages in the database"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender_id = data.get("sender_id")
            receiver_id = data.get("receiver_id")
            message_text = data.get("message")

            if not sender_id or not receiver_id:
                return JsonResponse({"status": "error", "message": "Sender or Receiver ID is missing"}, status=400)

            sender_user = com_TB.objects.filter(id=sender_id).first()
            receiver_service = Service_DB.objects.filter(id=receiver_id).first()

            if not sender_user or not receiver_service:
                return JsonResponse({"status": "error", "message": "Invalid sender or receiver"}, status=400)

            message = Messages_Tb.objects.create(
                sender_user=sender_user,
                receiver_service=receiver_service,
                message=message_text,
                timestamp=now(),
                is_read=False
            )

            return JsonResponse({"status": "success", "message_id": message.id})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def get_messages(request):
    # ✅ Get user ID from session or manually from request
    user_id = request.session.get("user_id") or request.GET.get("user_id")

    # ✅ Ensure user_id is a valid integer
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid user_id. It must be a number."}, status=400)

    try:
        # ✅ Get all messages where the user is either the sender or receiver
        messages = Messages_Tb.objects.filter(
            Q(sender_user_id=user_id) | Q(receiver_user_id=user_id)
        ).order_by("timestamp")

        service_last_messages = []
        unique_services = set()

        # ✅ Extract the latest message for each unique service the user chatted with
        for msg in messages:
            sender_id = msg.sender_service.id if msg.sender_service else None
            receiver_id = msg.receiver_user.id if msg.receiver_user else None
            service_id = sender_id if sender_id else receiver_id  

            if service_id and service_id not in unique_services:
                unique_services.add(service_id)
                service_last_messages.append({
                    "service_id": service_id,
                    "last_message": msg.message,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                })

        # ✅ Sort last messages in descending order
        service_last_messages.sort(
            key=lambda x: x["timestamp"], 
            reverse=True
        )

        # ✅ Convert all messages to JSON format
        message_data = [
            {
                "sender": msg.get_sender() if msg.get_sender() else "Unknown",
                "sender_id": msg.sender_user.id if msg.sender_user else (msg.sender_service.id if msg.sender_service else None),
                "message": msg.message,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_read": msg.is_read,
            }
            for msg in messages
        ]

        return JsonResponse({
            "messages": message_data,
            "service_last_messages": service_last_messages,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

       


from django.http import JsonResponse
from service.models import Service_DB

def get_services(request):
    query = request.GET.get("q", "")
    services = Service_DB.objects.filter(CentreName__icontains=query)[:10]
    
    service_list = [{"id": s.id, "CentreName": s.CentreName, "Location": s.Location} for s in services]
    
    return JsonResponse({"services": service_list})


from django.db.models import Q
from django.http import JsonResponse
from .models import Messages_Tb
from service.models import  Service_DB  # Ensure Service_Tb is imported

def get_recent_chats(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({"error": "User not logged in"}, status=401)

    # Fetch distinct chats where user was either sender or receiver
    recent_chats = Messages_Tb.objects.filter(
        Q(sender_user_id=user_id) | Q(receiver_service_id=user_id)
    ).values("sender_user_id", "receiver_service_id").distinct()

    chats_list = []
    for chat in recent_chats:
        # Determine the other party in the conversation
        service_id = chat["receiver_service_id"] if chat["sender_user_id"] == user_id else chat["sender_user_id"]
        
        # Fetch the service name from Service_Tb
        service = Service_DB.objects.filter(id=service_id).first()
        service_name = service.CentreName if service else "Unknown Service"
        
        chats_list.append({
            "id": service_id,
            "name": service_name
        })

    return JsonResponse({"recent_chats": chats_list})





#SERVICE CENTER VIEWS
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Messages_Tb
import traceback

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Messages_Tb
import traceback

@login_required
def service_chat(request):
    service_id = request.session.get("id")  # Assuming service ID is stored in session

    # Fetch distinct users who have messaged the service
    user_chats = Messages_Tb.objects.filter(receiver_service_id=service_id) \
        .values("sender_user_id", "sender_user__FullName").distinct()

    users = [{"id": chat["sender_user_id"], "name": chat["sender_user__FullName"]} for chat in user_chats]

    return render(request, "chat/service_chat.html", {"users": users})


from django.http import JsonResponse
from django.db.models import Q, Max
from .models import Messages_Tb

def get_service_messages(request):
    """Fetch messages for a service and the latest message from each user."""
    
    # ✅ Get service ID from session or request
    service_id = request.session.get("id") or request.GET.get("service_id")

    # ✅ Ensure service_id is a valid integer
    try:
        service_id = int(service_id)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid service_id. It must be a number."}, status=400)

    try:
        # ✅ Fetch latest messages per user
        last_messages = (
            Messages_Tb.objects
            .filter(Q(receiver_service_id=service_id) | Q(sender_service_id=service_id))
            .values("sender_user_id")
            .annotate(last_message_time=Max("timestamp"))  # Get latest timestamp per user
            .order_by("-last_message_time")  # Sort by latest message
        )

        user_last_messages = []
        for msg in last_messages:
            user_last_messages.append({
                "user_id": msg["sender_user_id"],
                "last_message_time": msg["last_message_time"].strftime("%Y-%m-%d %H:%M:%S"),
            })

        # ✅ Fetch all messages involving the service (optimized)
        messages = (
            Messages_Tb.objects
            .filter(Q(receiver_service_id=service_id) | Q(sender_service_id=service_id))
            .order_by("timestamp")
            .values("sender_user_id", "message", "timestamp", "is_read")  # Fetch only necessary fields
        )

        # ✅ Format messages for JSON response
        message_data = [
            {
                "sender_id": msg["sender_user_id"],
                "message": msg["message"],
                "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                "is_read": msg["is_read"],
            }
            for msg in messages
        ]

        return JsonResponse({
            "messages": message_data,
            "user_last_messages": user_last_messages,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



import json
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Messages_Tb  # Ensure this import is correct

@login_required
@csrf_exempt  # ⚠️ Only use if CSRF protection is already handled elsewhere!
def service_send_message(request):
    """
    Service sends a message to a user.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))  # Handles JSON data
            service_id = request.session.get("id")  # Ensure the service is logged in
            user_id = data.get("user_id")  # Ensure user ID is provided
            text = data.get("message")  # Ensure message is provided

            if not service_id:
                return JsonResponse({"error": "Service not authenticated"}, status=403)

            if not user_id:
                return JsonResponse({"error": "Receiver user ID is required"}, status=400)

            if not text:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            # Save the message to the database
            Messages_Tb.objects.create(
                sender_service_id=service_id,
                receiver_user_id=user_id,
                message=text  # Ensure the field name is correct in your model
            )

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            print(traceback.format_exc())  # Logs the full error in the console
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)




@login_required
def get_service_recent_chats(request):
    """
    Get recent users the service has chatted with.
    """
    try:
        service_id = request.session.get("service_id")

        sent_chats = list(Messages_Tb.objects.filter(sender_service_id=service_id)
                          .values("receiver_user_id", "receiver_user__FullName").distinct())

        received_chats = list(Messages_Tb.objects.filter(receiver_user_id=service_id)
                              .values("sender_service_id", "sender_service__CentreName").distinct())

        recent_list = []
        for chat in sent_chats:
            if chat["receiver_user_id"] and chat["receiver_user__FullName"]:
                recent_list.append({
                    "id": chat["receiver_user_id"],
                    "name": chat["receiver_user__FullName"],
                })

        for chat in received_chats:
            if chat["sender_service_id"] and chat["sender_service__CentreName"]:
                recent_list.append({
                    "id": chat["sender_service_id"],
                    "name": chat["sender_service__CentreName"],
                })

        recent_list = list({item["id"]: item for item in recent_list}.values())

        return JsonResponse({"recent_chats": recent_list})

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)


from django.db.models import Q

@login_required
def get_service_chat_users(request):
    """API to fetch users who have chatted with the service"""
    service_id = request.session.get("id")

    if not service_id:
        return JsonResponse({"error": "Service ID not found in session"}, status=400)

    # Fetch users who have either sent or received messages with this service
    user_chats = Messages_Tb.objects.filter(
        Q(receiver_service_id=service_id) | Q(sender_service_id=service_id)
    ).values("sender_user_id", "sender_user__FullName").distinct()

    users = [{"id": chat["sender_user_id"], "name": chat["sender_user__FullName"]} for chat in user_chats if chat["sender_user_id"]]

    return JsonResponse({"users": users})
