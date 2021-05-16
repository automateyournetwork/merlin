Cisco has several APIs to get different information returned in JSON format. 

Using Merlin you can access these APIs, query the JSON output, and create business-ready documentation. 

[Support API](https://developer.cisco.com/site/support-apis/)

* Bug information
* TAC case information
* End-of-X information
* Product information
* RMA information
* Software Suggestion (Gold Star)

[Services API](https://developer.cisco.com/docs/service-apis/)

* Contracts and Coverage information
* Customer information
* Inventory information
* Product Alerts (Field Notice, Security Advisory, Security Vulnerability)

[Product Security Incident Reponse Team](https://developer.cisco.com/psirt/)

* Accelerate Cisco Security Vulnerability Assessments
* Customize Cisco Vulnerability Notifications
* Use Open Security Standards

[Business Critical Insights](https://developer.cisco.com/docs/business-critical-service-apis/)

BCI portal shows various key performance indicators, trends and predictive analytic insights. The data shown on the portal is now also available through APIs.

## Onboarding Process

### SmartNet Total Care (SNTC)

Cisco account must have API Developer role

1. Log in [Cisco.com](https://cisco.com)
2. Go to Manage Profile
3. Smart Services section
4. API Developer role = Active

If not, click on Contact Company Adminstrator to know who to ask to get it.

### Cisco API console

Create an application add assign APIs

* Log in [Cisco API console](https://apiconsole.cisco.com)
* Go to My Apps & Keys
* Register a New App

  * Name of your application: <Name Your Application>
  * OAuth2.0 Credentials: Client Credentials

* Save
* Add APIs to the application

  * Software Suggestion API V2
  * Serial Number to Information
  * PSIRT 

* I agree to the terms and service
* Save

Please take note of:

* KEY: OAuth2.0 {{ client_id }}
* CLIENT_SECRET: OAuth2.0 {{ client_secret }}

# Merlin Magic

Update the API Credentials file with your keys and secrets. It is a good idea to use Secret Strings and encrypt the secrets. 

    APIs:
        recommended_release:
            recommended_release_api_username: {{ your key here }}
            recommended_release_api_password: {{ your secret here }}
        serial_2_info:
            serial_2_info_api_username: {{ your key here }}
            serial_2_info_api_password: {{ your secret here }}
        psirt:
            psirt_api_username: {{ your key here }}
            psirt_api_password: {{ your secret here }}

Update the testbed_cisco_api.yaml to reflect your topology and devices. 

Run the pyATS job

```console
pyats run job Cisco_API_merlin_job.py --testbed-file testbed/testbed_cisco_api.yaml
```

[Back to the main project](https://github.com/automateyournetwork/merlin)