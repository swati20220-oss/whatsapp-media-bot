from whatsapp_api_client_python import API
import time

# ⚠️ Yahan apni Green-API ki details dalein
ID_INSTANCE = "YAHAN_APNI_ID_INSTANCE_DALEIN"
API_TOKEN_INSTANCE = "YAHAN_APNA_API_TOKEN_INSTANCE_DALEIN"

# ⚠️ Yahan apne target WhatsApp Group ki ID dalein (Example: '120363xxxxxx@g.us')
TARGET_GROUP_ID = "YAHAN_GROUP_ID_DALEIN@g.us"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

print("WhatsApp Bot starting and watching for messages...")

# Puraane messages ko skip karne ke liye list
seen_messages = set()

while True:
    try:
        # Green-API se naye messages check karna
        receive_response = greenAPI.receiving.receiveNotification()
        
        if receive_response.code == 200 and receive_response.data:
            notification = receive_response.data
            id_webhook = notification.get("idMessage")
            body = notification.get("messageData", {})
            
            # Agar message media hai (Photo/Video) aur pehle nahi dekha gaya
            if id_webhook not in seen_messages:
                seen_messages.add(id_webhook)
                
                type_msg = body.get("typeMessage")
                
                # Check agar photo ya video hai
                if type_msg in ["imageMessage", "videoMessage"]:
                    print(f"Media message mila! Type: {type_msg}")
                    
                    # Us media ko seedha target group me forward/send karna
                    # Hum message ka URL ya file lekar target par bhej rahe hain
                    file_url = body.get("fileMessageData", {}).get("downloadUrl")
                    file_name = body.get("fileMessageData", {}).get("fileName", "media")
                    
                    if file_url:
                        greenAPI.sending.sendFileByUrl(
                            chatId=TARGET_GROUP_ID,
                            urlFile=file_url,
                            fileName=file_name,
                            caption="Forwarded via Bot"
                        )
                        print("Media successfully forwarded to group!")
                        
            # Notification ko delete karna taaki server par load na bade
            greenAPI.receiving.deleteNotification(notification.get("receiptId"))
            
    except Exception as e:
        print(f"Koi error aaya bhai: {e}")
        
    # Server par zyada load na pade isiliye har 3 second me check karega
    time.sleep(3)
