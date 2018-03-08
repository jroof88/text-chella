from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/textChella")
def response():
    resp = MessagingResponse()
    
    incoming_number = request.form['From']
    
    #if is_user(incoming_number) == false:
        #subscribe_user(incoming_number)
        #resp.message(send_todays(incoming_number))
        #return str(resp)
    #else:
        #return ''
        
if __name__ == "__main__":
    app.run(debug=True)