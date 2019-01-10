from flask import Flask, request, redirect, render_template
from text_chella import is_user, subscribe, delete_user
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/textChella", methods=['POST', 'GET'])
def response():
    resp = MessagingResponse()

    incoming_number = request.form['From']
    incoming_message = request.form['Body']

    blacklist_words = ["STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"]
    
    if incoming_message.upper() in blacklist_words:
        delete_user(incoming_number)
        return ''
    else:
        if is_user(incoming_number) == False:
            msg = subscribe(incoming_number)
            resp.message(msg)
            return str(resp)
        else:
            return ''


if __name__ == "__main__":
    app.run(debug=True)

