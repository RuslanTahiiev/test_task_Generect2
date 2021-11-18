import json
import os

import requests

RESULT_DIR = 'result'
RESULT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULT_DIR)


class Hub:

    _headers = {
            'Accept': 'text/html, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0)Gecko/20100101 Firefox/93.0'
        }

    '''
    URL of test server for requests. Deployed at Heroku.
    Repo at https://github.com/RuslanTahiiev/test_server
    '''
    _url = 'https://testserverfortesttask.herokuapp.com/'

    @classmethod
    def get_req(cls, params):
        '''
            GET request
            :param params:
            :type params: str
            :return data: json
        '''
        url_ = cls._url + params
        response = requests.get(url_)
        response.raise_for_status()
        if response.status_code != 204:
            response = json.loads(requests.get(url=url_, headers=cls._headers).text)
            return response


class Lead:
    def __init__(self, full_name, job_title, profile_url, location, email, phone_number):
        self.full_name = full_name
        self.job_title = job_title
        self.profile_url = profile_url
        self.location = location
        self.email = email
        self.phone_number = phone_number

    def add_lead_to_company(self):
        return self._format_json()

    def _format_json(self):
        return {
                "full_name": self.full_name,
                "job_title": self.job_title,
                "profile_url": self.profile_url,
                "location": self.location,
                "email": self.email,
                "phone_number": self.phone_number
            }


class Company:

    def __init__(self, name, company_url, location, revenue):
        self.name = name
        self.company_url = company_url
        self.location = location
        self.revenue = revenue
        self.leads = []

    def __repr__(self):
        return f'{self.name} in list!\n'

    def create_company_report(self):
        self._create_data()

        if not os.path.exists(RESULT_ROOT):
            os.mkdir(RESULT_ROOT)

        print(RESULT_ROOT)

        with open(f'{RESULT_ROOT}/{self.name}_report.json', 'w', encoding='utf-8') as file:
            json.dump(self._format_json(), file, indent=4, ensure_ascii=False)

        return self._format_json()

    def _format_json(self):
        return {
                "name": self.name,
                "company_url": self.company_url,
                "location": self.location,
                "revenue": self.revenue,
                "leads": self.leads
            }

    def _create_data(self):
        persons = Hub.get_req('list_of_persons')
        for person in persons:
            if person['company_fk'] == self.company_url:
                param = person['profile_url']
                data = Hub.get_req(f'person?pk={param}')
                lead = Lead(
                    full_name=data['full_name'],
                    job_title=data['job_title'],
                    profile_url=data['profile_url'],
                    location=data['location'],
                    email=data['email'],
                    phone_number=data['phone_number']
                )
                self.leads.append(lead.add_lead_to_company())
                print('Success!')


class Searcher:
    '''
        Enter point
    '''
    def __init__(self):
        self.companies = Hub.get_req('list_of_companies')

    def go(self):
        self.__parser_list_of_companies()

    def __parser_list_of_companies(self):
        for c in self.companies:
            param = c['company_url']
            company = Hub.get_req(F'company?pk={param}')
            company_obj = Company(
                    name=company['name'],
                    company_url=company['company_url'],
                    location=company['location'],
                    revenue=company['revenue']
            )
            print('Create company report for: ', company_obj)
            company_obj.create_company_report()
        print('Done!')

