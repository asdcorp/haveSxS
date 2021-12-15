from havesxs import generate_sxs_name

#amd64_microsoft-windows-servicingstack_31bf3856ad364e35_10.0.19041.1_none_bf506ecc66a800df
#amd64_microsoft-windows-servicingstack_31bf3856ad364e35_none_4a207b402ad93a1c
servicingstack = {
    'name': 'Microsoft-Windows-ServicingStack',
    'culture': 'none',
    'version': '10.0.19041.1',
    'publicKeyToken': '31bf3856ad364e35',
    'processorArchitecture': 'amd64',
    'versionScope': 'nonSxS'
}

print(generate_sxs_name(servicingstack))
print(generate_sxs_name(servicingstack, winners=True))


#amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.19041.1110_none_60b5254171f9507e
#amd64_microsoft.windows.common-controls_6595b64144ccf1df_none_62fe57338acfab7a
commoncontrols = {
    'name': 'Microsoft.Windows.Common-Controls',
    'culture': 'none',
    'version': '6.0.19041.1110',
    'publicKeyToken': '6595b64144ccf1df',
    'processorArchitecture': 'amd64',
    'type': 'win32'
}

print(generate_sxs_name(commoncontrols))
print(generate_sxs_name(commoncontrols, winners=True))
