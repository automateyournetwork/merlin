from requests_ntlm import HttpNtlmAuth

#Enter your SharePoint site and target library
sharePointUrl = 'https://mydomain.com'
folderUrl = '/DocumentLibrary/Camelot/'

# Show version Example
if hasattr(self, 'parsed_show_version'):
    sh_ver_template = env.get_template('show_version.j2')

    with open("Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.json" % device.alias, "w") as fid:
        json.dump(self.parsed_show_version, fid, indent=4, sort_keys=True)

    with open("Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.yaml" % device.alias, "w") as yml:
        yaml.dump(self.parsed_show_version, yml, allow_unicode=True)

    for filetype in filetype_loop:
        parsed_output_type = sh_ver_template.render(to_parse_version=self.parsed_show_version['version'],filetype_loop_jinja2=filetype)

        with open("Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.%s" % (device.alias,filetype), "w") as fh:
            fh.write(parsed_output_type)

        if os.path.exists("Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.md" % device.alias):
            os.system("markmap --no-open Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.md --output Camelot/Cisco/IOS_XE/Show_Version/%s_show_version_mind_map.html" % (device.alias,device.alias))
    
    ##############
    # SHAREPOINT #
    ##############

    #Read filename (relative path) from command line
    sharePointFileName = "Camelot/Cisco/IOS_XE/Show_Version/%s_show_version.csv" % device.alias
    uploadFileName = "%s_show_version.csv" % device.alias 

    # Sets up the url for requesting a file upload
    requestUrl = sharePointUrl + '/_api/web/getfolderbyserverrelativeurl(\'' + folderUrl + '\')/Files/add(url=\'' + uploadFileName + '\',overwrite=true)'
    
    # Read in the file that we are going to upload
    file = open(sharePointFileName, 'rb')

    # Setup the required headers for communicating with SharePoint 
    headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose'}

    # Execute a request to get the FormDigestValue. This will be used to authenticate our upload request
    r = requests.post(sharePointUrl + "/_api/contextinfo",auth=HttpNtlmAuth('DOMAIN\\USERNAME','PASSWORD'), headers=headers)
    formDigestValue = r.json()['d']['GetContextWebInformation']['FormDigestValue']

    # Update headers to use the newly acquired FormDigestValue
    headers = {'Content-Type': 'application/json; odata=verbose', 'accept': 'application/json;odata=verbose', 'x-requestdigest' : formDigestValue}

    # Execute the request. If you run into issues, inspect the contents of uploadResult
    uploadResult = requests.post(requestUrl,auth=HttpNtlmAuth('DOMAIN\\USERNAME','PASSWORD'), headers=headers, data=file.read())