import requests
import json
from bs4 import BeautifulSoup

urls = {
    'HOME_URL' : 'https://erp.iitkgp.ernet.in/IIT_ERP3/welcome.jsp',
    'AUTH_URL' :'https://erp.iitkgp.ernet.in/SSOAdministration/auth.htm',
    'SECURITYQ_URL' : 'https://erp.iitkgp.ernet.in/SSOAdministration/getSecurityQues.htm',
    'TP_URL' : 'https://erp.iitkgp.ernet.in/TrainingPlacementSSO/TPStudent.jsp',
    'SSO_URL' : 'https://erp.iitkgp.ernet.in/IIT_ERP3/showmenu.htm',
    'CV_URL' : "https://erp.iitkgp.ernet.in/TrainingPlacementSSO/AdmFilePDF.htm?path=/DATA/ARCHIVE/TRAINGANDPLACEMNT/STUDENT/{0}/RESUME/1.pdf",
    'LOGOUT_URL' : 'https://erp.iitkgp.ernet.in/IIT_ERP3/logout.htm'
}

# get credentials from json
with open('credentials.json','r') as f:
    details = json.load(f)
    auth  = {
        'USER_ID' : details['USER_ID'],
        'USER_PASSWORD' : details['USER_PASSWORD'],
        'SECURITY_ANSWERS' : details['SECURITY_ANSWERS']
    }

def login():
    ''' This function returns the session object that has all the cookies you need for retrieving data from erp.'''
    s = requests.Session()
    r = s.get(urls['HOME_URL'])
    soup = BeautifulSoup(r.text, "html5lib")
    sessionToken = soup.find(id='sessionToken').get('value')   
    r = s.post(urls['SECURITYQ_URL'], data = {'user_id': auth['USER_ID'] })
    if r.status_code != 200:
        return False
    security_answer = auth['SECURITY_ANSWERS'][r.text]
    

    login_data = { 
        'user_id' : auth['USER_ID'],
        'password' : auth['USER_PASSWORD'],
        'answer' : security_answer,
        'sessionToken' : sessionToken,
        'requestedUrl' : urls['HOME_URL']
    }

    r = s.post(urls['AUTH_URL'], data = login_data)

    tnp_data = {
        'module_id' : '26',
        'menu_id' : '11',
        'link' : 'https://erp.iitkgp.ernet.in/TrainingPlacementSSO/TPStudent.jsp',
        'delegated_by': '',
        'module_name' : 'CDC',
        'parent_display_name' : 'Student',
        'display_name' : 'Application of Placement/Internship'
    }

    r = s.post(urls['SSO_URL'], data=tnp_data)
    soup2 = BeautifulSoup(r.text, "html5lib")
    ssoToken = soup2.find(id='ssoToken').get('value')

    sso_data = {
        'ssoToken' : ssoToken,
        'module_id' : '26',
        'menu_id' : '11'
    }

    s.post(urls['TP_URL'], data = sso_data)
    return s


if __name__ == '__main__':
    s = login()
