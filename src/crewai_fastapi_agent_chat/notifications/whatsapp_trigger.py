import requests
def whati(data):
    # Prepare the request body
    print("whatsapp",data)
    payload = {
        "messageType": "text",
        "mobile": f"91{data['mobile_number']}",
         "messagContent": f"""
🌟 *Agent Chat* 🌟

👋 Hi {data['user_name']},

Here is the file you requested:  
📎 {data['file_url']}

If you have any questions, feel free to reach out.  

🤝 *Best Regards,*  
*Treeone Team* 🌿
        """,
        "phoneNumberId":"404750372717022"
    }
    reqUrl="https://pura.treeone.one/fb_wa/send_message"

    try:
        response = requests.post(reqUrl, data=payload)
        print(">>>>>>>>>>>>>>>",response.json())
        # Check the response status code
        if response.status_code == 200:
            print("Whatsapp send successfully!")
            print("Response Content:", response.json())
            return f"✅ Whatsapp send successfully to {data['mobile_number']}"
        else:
            print("Failed to send Whatsapp. Status Code:", response.status_code)
            print("Response Content:", response.text)
            return "Failed to send Whatsapp"

    except requests.exceptions.RequestException as e:
        print("An error occurred while sending the Whatsapp:", e)

# whati({"mobile_number":"7010329187","user_name":"Antony","file_url":"https://crediwise.nte.ai/file/viewFile/6601623a14410e9e0639519f"})