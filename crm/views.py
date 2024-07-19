import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages

####################################  Login  ################################################
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # api_url = "http://13.233.211.102/masters/api/login/"
        api_url = "https://vgold.app/vgold_admin/api/login/"
        
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            print(response_data)
            
            if response_data.get('message_code') == 1000:
                # messages.success(request, response_data.get('message_text'))
                # Store only message_data in session
                request.session['user'] = response_data.get('message_data', {})
                print( request.session['user'])
                return redirect('dashboard')  # Redirect to dashboard after successful login# Redirect to login page after successful login
            else:
                messages.error(request, response_data.get('message_text', 'Login failed.'))
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")
    
    return render(request, 'crm/login.html')

####################################  Dashboard  ################################################
def dashboard(request):
    # Retrieve user data from session if available
    user_data = request.session.get('user', {})
    username = user_data.get('first_name', '')
    user_id = user_data.get('id', '')

    context = {
        'username': username,
        'user_id': user_id,
    }
    return render(request, 'crm/dashboard.html', context)


####################################  Add Lead  ################################################
def add_lead(request):
     # Retrieve user data from session if available
    user_data = request.session.get('user', {})
    user_id = user_data.get('id', '')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        source = request.POST.get('source')
        city = request.POST.get('city')
        comment = request.POST.get('comment')
        
        payload={
            "lead_name":name,
            "lead_email":email,
            "lead_contact_no":contact,
            "comment":comment,
            "lead_city":city,
            "lead_source":source,
            "lead_by_id":user_id,
            "lead_handler_id":user_id,
        }
        # print(payload)
        # api_url = "http://13.233.211.102/masters/api/insert_lead/"
        api_url = "https://vgold.app/vgold_admin/api/insert_lead/"
     
        try:
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            # print(response_data)
            
            if response_data.get('message_code') == 1000:
                messages.success(request, response_data.get('message_text'))
                return redirect('view_lead')  # Redirect to dashboard after successful login# Redirect to login page after successful login
            else:
                messages.error(request, response_data.get('message_text', 'Data not Insert or submit'))
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")
    
    return render(request, 'crm/add_lead.html')

####################################  View Lead ################################################
def view_lead(request):
    # Retrieve user data from session if available
    user_data = request.session.get('user', {})
    user_id = user_data.get('id', '')
    
    # API URL and parameters
    # api_url = 'http://13.233.211.102/masters/api/get_leads_by_handler_or_by_id/'
    
    api_url = 'https://vgold.app/vgold_admin/api/get_leads_by_handler_or_by_id/'
    params = {
        'lead_by_id': user_id
    }
    
    # Making the API request
    response = requests.post(api_url, json=params)
    
    # print(response.text)
    
    if response.status_code == 200:
        leads_data = response.json().get('message_data', [])
        # print(leads_data)
    else:
        leads_data = []  # Handle error scenario
    
    # Render the template with leads data
    return render(request, 'crm/view_lead.html', {'leads_data': leads_data})

####################################  Lead Edit  ################################################
def lead_edit(request, id):
    if (request.method=='GET'):
        # Print the incoming ID parameter
        print(id)
        
        # API endpoint URL
        # api_url = "http://13.233.211.102/masters/api/get_lead_by_id/"
        api_url = "https://vgold.app/vgold_admin/api/get_lead_by_id/"
        
        # Data to be sent in the POST request
        data = {
            "lead_id": id
        }
        
        # Sending POST request to the API
        response = requests.post(api_url, data=data)
        
        # Check if API request was successful
        if response.json().get('message_code') == 1000:
            api_data = response.json()
            lead_data = api_data.get('message_data', {})
            # print(lead_data)
            # Rendering the template with lead data
            return render(request, 'crm/lead_edit.html', {'lead_data': lead_data})
        
        else:
            # Handle API request failure
            return JsonResponse({'error': 'Failed to fetch lead data'}, status=response.status_code)
        
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        source = request.POST.get('source')
        city = request.POST.get('city')
        comment = request.POST.get('comment')
        
        payload={
            "lead_name":name,
            "lead_email":email,
            "lead_contact_no":contact,
            "comment":comment,
            "lead_city":city,
            "lead_source":source,
            "lead_id": id,
        }
        
        print(payload)
        
        # print(payload)
        # api_url = "http://13.233.211.102/masters/api/update_lead/"
        
        api_url = "https://vgold.app/vgold_admin/api/update_lead/"
     
        try:
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            # print(response_data)
            
            if response_data.get('message_code') == 1000:
                messages.success(request, response_data.get('message_text'))
                return redirect('view_lead')  # Redirect to dashboard after successful login# Redirect to login page after successful login
            else:
                messages.error(request, response_data.get('message_text', 'Data not Insert or submit'))
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")
            
###################################### Logout #############################################
def add_followup(request,id):
    
    if (request.method=='GET'):
        # Print the incoming ID parameter
        print(id)
        
        # API endpoint URL
        # api_url = "http://13.233.211.102/masters/api/get_lead_by_id/"
        
        api_url = "https://vgold.app/vgold_admin/api/get_lead_by_id/"
        
        # Data to be sent in the POST request
        data = {
            "lead_id": id
        }
        
        # Sending POST request to the API
        response = requests.post(api_url, data=data)
        
        # Check if API request was successful
        if response.json().get('message_code') == 1000:
            api_data = response.json()
            lead_data = api_data.get('message_data', {})
            # print(lead_data)
            # Rendering the template with lead data
            return render(request, 'crm/add_followup.html', {'lead_data': lead_data})
        
        else:
            # Handle API request failure
            return JsonResponse({'error': 'Failed to fetch lead data'}, status=response.status_code)
        
    else:
         # Retrieve user data from session if available
        user_data = request.session.get('user', {})
        user_id = user_data.get('id', '')
        followup_datetime = request.POST.get('followup_datetime')
        followup_method = request.POST.get('followup_method')
        follow_up_details = request.POST.get('follow_up_details')
        followup_status = request.POST.get('followup_status')
        next_follow_up_date_time_stamp = request.POST.get('next_follow_up_date_time_stamp')
        next_followup_method = request.POST.get('followup_method')
        next_follow_up_details = request.POST.get('next_follow_up_details')
        
        payload={
            "lead_id": id,
            "follow_up_date_time_stamp":followup_datetime,
            "follow_up_method":followup_method,
            "follow_up_details":follow_up_details,
            "follow_up_success_status":followup_status,
            "next_follow_up_date_time_stamp":next_follow_up_date_time_stamp,
            "next_follow_up_method":next_followup_method,
            "next_follow_up_action": next_follow_up_details,
            "follow_up_by": user_id,
            "follow_up_user_id": user_id,   
        }
        
        # print(payload)

        # api_url = "http://13.233.211.102/masters/api/insert_lead_followup/"
        api_url = "https://vgold.app/vgold_admin/api/insert_lead_followup/"
     
        try:
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            # print(response_data)
            
            if response_data.get('message_code') == 1000:
                messages.success(request, response_data.get('message_text'))
                return redirect('view_lead')  # Redirect to dashboard after successful login# Redirect to login page after successful login
            else:
                messages.error(request, response_data.get('message_text', 'Data not Insert or submit'))
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {e}")
        
###################################### Logout #############################################
import requests
from django.shortcuts import render
from django.http import JsonResponse

def view_followup(request, id):
    if request.method == 'GET':
        # Print the incoming ID parameter
        user_data = request.session.get('user', {})
        user_name = user_data.get('username', '')
        
        print(id)
        
        # API endpoint URLs
        # lead_api_url = "http://13.233.211.102/masters/api/get_lead_by_id/"
        # followup_api_url = "http://13.233.211.102/masters/api/get_followups_by_lead_id/"
        
        lead_api_url = "https://vgold.app/vgold_admin/api/get_lead_by_id/"
        followup_api_url = "https://vgold.app/vgold_admin/api/get_followups_by_lead_id/"
        
        # Data to be sent in the POST requests
        lead_data = {"lead_id": id}
        followup_data = {"lead_id": id}
        
        # Sending POST requests to the APIs
        lead_response = requests.post(lead_api_url, data=lead_data)
        followup_response = requests.post(followup_api_url, data=followup_data )
        
        # Check if API requests were successful
        if lead_response.json().get('message_code') == 1000:
            lead_api_data = lead_response.json().get('message_data', {})
        else:
            return JsonResponse({'error': 'Failed to fetch lead data'}, status=lead_response.status_code)
        
        if followup_response.json().get('message_code') == 1000:
            followup_api_data = followup_response.json().get('message_data', [])
        else:
            print(followup_response.text)
            messages.error(request,  followup_response.json().get('message_text', []))
            return render(request, 'crm/view_followup.html', {'lead_data': lead_api_data , "user_name":user_name})

        # print(lead_api_data)
        print(followup_api_data)
        # Rendering the template with lead and follow-up data
        return render(request, 'crm/view_followup.html', {'lead_data': lead_api_data, 'followup_data': followup_api_data , "user_name":user_name})
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

        
###################################### Logout #############################################
def Logout(request):
    # Clear all sessions
    request.session.clear()
    # Redirect to the login page
    return redirect('login')
