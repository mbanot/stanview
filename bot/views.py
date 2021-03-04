from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from . import scenarios


@csrf_exempt
def webhook(request):
    response = MessagingResponse()

    def bye():
        message = f" Thank you for chatting with us...\n" \
                  f" Have a good day! \n"
        del(request.session['function'])
        response.message(message)

    def hi():
        message = f" * Hi* \n" \
                  f" *Welcome to Stanview!* \n\n" \
                  f" 1>Fault follow up/ registration \n" \
                  f" 2>Account status enquiry \n" \
                  f" 3>Request to speak to an agent \n" \
                  f" 4>Exit \n"
        request.session['function'] = 'menu'
        response.message(message)

    def fault_menu():
        message = f" What would you like to do? \n" \
                  f" 1>Follow up \n" \
                  f" 2>Register \n" \
                  f" 0>Home \n"
        request.session['function'] = 'follow/register'
        response.message(message)

    def enquiry_menu():
        message = f" You have chosen account status enquiry \n" \
                  f" 0>Home \n"
        request.session['function'] = 'enquiry'
        response.message(message)

    def agent_menu():
        message = f" How do you wish to communicate with our agent? \n" \
                  f" 1>Website \n" \
                  f" 2>LiveChat \n" \
                  f" 3>Call \n" \
                  f" 0>Home \n"
        request.session['function'] = 'agent'
        response.message(message)

    def menu():
        body = request.POST.get("Body")
        if body == '1':
            fault_menu()
        elif body == '2':
            enquiry_menu()
        elif body == '3':
            agent_menu()
        elif body == '4':
            bye()
        else:
            hi()

    def follow_register():
        body = request.POST.get("Body")
        if body == '1':
            message = f" Please enter the fault number: \n"
            request.session['function'] = 'follow'
            response.message(message)
        elif body == '2':
            message = f" New Fault Registration \n" \
                      f" 0>Home \n"
            request.session['function'] = 'register_fault'
            response.message(message)
        elif body == '0':
            hi()
        else:
            fault_menu()

    def agent():
        body = request.POST.get("Body")
        if body == '1':
            message = f" Website is ...: \n"
            request.session['function'] = 'website'
            response.message(message)
        elif body == '2':
            message = f" Follow this link ... \n"
            request.session['function'] = 'live_chat'
            response.message(message)
        elif body == '3':
            message = f" 0777470333/ 0782384322 \n"
            request.session['function'] = 'call'
            response.message(message)
        elif body == '0':
            hi()
        else:
            agent_menu()

    if request.method == "POST":

        if request.session.get('function') == 'menu':
            menu()
        elif request.session.get('function') == 'follow/register':
            follow_register()
        elif request.session.get('function') == 'agent':
            agent()
        else:
            hi()

    return HttpResponse(response.to_xml(), content_type='text/xml')


