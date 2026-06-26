from whatsapp_api_client_python import API
import time

# ⚠️ Yahan apni Green-API ki details dalein
ID_INSTANCE = "7107664970"
API_TOKEN_INSTANCE = "6aa8b6ada5bd43f2a97abc63a2272c0f65434541b49e4afca4"

# ⚠️ SOURCE_GROUP_ID = Jahan se photo/video UTHANI hai (Example: '120363xxxx@g.us')
SOURCE_GROUP_ID = "120363427921537759@g.us"

# ⚠️ TARGET_GROUP_ID = Jahan photo/video BHEJNI hai (Example: '120363xxxx@g.us')
TARGET_GROUP_ID = "120363405481516191@g.us"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

print("WhatsApp Bot chalu ho gaya hai...")
seen_messages = set()

while True:
    try:
        receive_response = greenAPI.receiving.receiveNotification()
        
        if receive_response.code == 200 and receive_response.data:
            notification = receive_response.data
            id_webhook = notification.get("idMessage")
            body = notification.get("messageData", {})
            
            # Pata karo message kis group se aaya hai
            sender_chat_id = notification.get("senderData", {}).get("chatId")
            
            # SIRF tabhi chalega jab message hamare SOURCE group se aayega aur naya hoga
            if sender_chat_id == SOURCE_GROUP_ID and id_webhook not in seen_messages:
                seen_messages.add(id_webhook)
                
                type_msg = body.get("typeMessage")
                
                # Check agar photo ya video hai
                if type_msg in ["imageMessage", "videoMessage"]:
                    print(f"Naya media mila! Type: {type_msg}")
                    
                    file_url = body.get("fileMessageData", {}).get("downloadUrl")
                    file_name = body.get("fileMessageData", {}).get("fileName", "media")
                    
                    if file_url:
                        # Target group me forward karein
                        greenAPI.sending.sendFileByUrl(
                            chatId=TARGET_GROUP_ID,
                            urlFile=file_url,
                            fileName=file_name,
                            caption="Forwarded via Bot"
                        )
                        print("Media successfully forward ho gaya!")
                        
            # Notification delete karein taaki loop sahi chale
            greenAPI.receiving.deleteNotification(notification.get("receiptId"))
            
    except Exception as e:
        print(f"Error aaya bhai: {e}")
        
    time.sleep(3)
