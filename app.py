from flask import Flask, request, redirect, render_template
from TextChella import is_user, subscribe
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/textChella", methods=['POST', 'GET'])
def response():
    resp = MessagingResponse()

    incoming_number = request.form['From']

    if is_user(incoming_number) == False:
        subscribe(incoming_number)
        #resp.message(send_todays(incoming_number))
        #return str(resp)
        return ''
    else:
        return ''

if __name__ == "__main__":
    app.run(debug=True)

