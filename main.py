import requests
from flask import Flask, request, jsonify
from flask.templating import render_template
import random
import json
import queue
import time
import threading

app = Flask(__name__, template_folder='template')
app.secret_key = "KarmaBeast"

header = {
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language':
    'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type':
    'application/json',
    'cookie':
    'C=0; O=0; V=fe1e774898a9e7b65927f05535ada8705f152e752524b9.90528389; optimizelyEndUserId=oeu1595223668906r0.027934908966102512; s_ecid=MCMID%7C60185159885597638692678916017568026992; _pxvid=9e914527-ca4b-11ea-873f-0242ac120007; _scid=c0e2ac1b-c16f-427c-b8f8-27515740bc3a; _ga=GA1.2.393893998.1595223673; _fbp=fb.1.1595223672826.978579793; _gcl_au=1.1.1989468470.1595223673; LPVID=NhNDcyZGRlM2VkZTc0NWIw; capp_promo_modal_shown=true; chgcsdetaintoken=1; _cs_c=1; gidr=MA; _fbc=fb.1.1599969124642.IwAR2Z_VnbjqNnsD1ZSHBH6JBGIt6Y8vleePHePlIWV46T8HrySaTg-TJC5d8; __gads=ID=f883ea08ff0a1d81:T=1595379471:R:S=ALNI_MaBxxG4YtrOaiGu_1x6Ac4NFu2MQw; gid=1565479; _rdt_uuid=1595423827407.d4ba5f79-eb95-42cb-99df-4fe73a0751ec; uuid230=d9d0fb2e-1924-4184-9188-aefa161dffe3; al_cell=main-1-control; _ym_uid=1614747935772498421; _ym_d=1614747935; adobeujs-optin=%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Atrue%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Atrue%2C%22target%22%3Atrue%2C%22mediaaa%22%3Atrue%7D; chgcsastoken=UWnWQm7kp32N_fR_Bl2RF-x7iHNErEbx898rP3W5R4qJd8i8zH_8RUngGZXvUqDbF5vJDQAcTpwrTcpQPYFLWmJ6ugip8PiORojxbW-VSV897aeI-UJYvuxB2DGceKC3; _gac_UA-499838-3=1.1617246489.CjwKCAjwu5CDBhB9EiwA0w6sLVoBK3rSmbC5yrXC8GVwB9gv4eZqVBsE6Mg4wzBSTZFvjgJgt_yf8RoCHN8QAvD_BwE; _gcl_aw=GCL.1617246492.CjwKCAjwu5CDBhB9EiwA0w6sLVoBK3rSmbC5yrXC8GVwB9gv4eZqVBsE6Mg4wzBSTZFvjgJgt_yf8RoCHN8QAvD_BwE; _gcl_dc=GCL.1617246492.CjwKCAjwu5CDBhB9EiwA0w6sLVoBK3rSmbC5yrXC8GVwB9gv4eZqVBsE6Mg4wzBSTZFvjgJgt_yf8RoCHN8QAvD_BwE; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%20fffd3170-ab55-4060-bb43-72e353855b73%2C%20%22created_date%22%20%3D%3E%202021-05-09T09%3A23%3A55.825Z%20%5D; U=50fb2356a4bd17ca93c19bc804c2141c; id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJmZmZkMzE3MC1hYjU1LTQwNjAtYmI0My03MmUzNTM4NTViNzMiLCJhdWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImV4cCI6MTYzNzE2NTM1NywiaWF0IjoxNjIxMzk1MzU3LCJlbWFpbCI6ImthdHJpbmEua2FsZUBhb2wuY29tIn0.nkd_VoRQWdORVK3uaHdStSPJPTOQw0gtoJi06iE-s-dICTUwsN7LIUhYU8TNjrm0kE7AdwhLlJFwkmaXxaUava0DUtddOrRTWPQ0Iq6ZFcBgtEFj8dGwIyMio3MIBIra77iX33f-eSVqBEDdgGtt_h5Q0yknXLmC5PYfe0GLVQPWIAvSvlE6HpK2SFukJLG4l-wQogTS4zYP7UJ6b247uhdvDl-L6UwcR4i5rHPWFE45SCV0Fdk7JtPU206JcVx9l03RLq8GZNI4XK9JdQ_mGWKHpJ_Yj1bMXjk6CiNJfIp4DS0VE1PhWZwk9Q45yVvedtfw2F5xPT4ujO7DuCFjWQ; _sctr=1|1621796400000; WRUID=3305402793935298; exp=A311C%7CA803B%7CA560B%7CA294C%7CA100B%7CA259B%7CA184B%7CA735B%7CC024C%7CA207A%7CA209A%7CA212A%7CA270C%7CA890H%7CA110B%7CA966C%7CA448A%7CA278C%7CA935A%7CA315B; expkey=00E1330B2980EA15068F08B99E91804A; intlPaQExitIntentModal=hide; _cs_id=6b30d022-fd86-ad2b-8d43-2d7961085730.1595392331.30.1622224873.1622224873.1.1629556331161.Lax.0; __CT_Data=gpv=102&ckp=tld&dm=chegg.com&apv_79_www33=102&cpv_79_www33=102&rpv_79_www33=5; PHPSESSID=645f3fda532bb900f26cd9f5db77d021; user_geo_location=%7B%22country_iso_code%22%3A%22PK%22%2C%22country_name%22%3A%22Pakistan%22%2C%22region%22%3A%22PB%22%2C%22region_full%22%3A%22Punjab%22%2C%22city_name%22%3A%22Bahawalpur%22%2C%22postal_code%22%3A%2263101%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ur-PK%22%5D%7D%7D; CSessionID=5f512007-5bc6-47ec-b538-3e9f43adb24f; SU=otOdLQtSyd0OCAx2u79a6LlTVwfFqn-OMAl2fBrI07alkcn98skdaN4x60HwG0YQqOTw1o6bE-OG-ejJHVb0EpwdkGWjuHX84XonZ_G0QMVeR-MVPbwcLswgt2G0WsFr; AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg=1; CVID=2f019103-d2d9-4f85-9481-a82cfe3deb56; _gid=GA1.2.1166389551.1622351555; opt-user-profile=fe1e774898a9e7b65927f05535ada8705f152e752524b9.90528389%252C19944471923%253A19956173008; OptanonConsent=isIABGlobal=false&datestamp=Sun+May+30+2021+18%3A18%3A45+GMT%2B0500+(Pakistan+Standard+Time)&version=6.10.0&hosts=&consentId=1e2fc7a1-fc85-4e09-b274-6753c9ef6c34&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; fffd3170-ab55-4060-bb43-72e353855b73_TMXCookie=true; _uetsid=a621fd30c10511eba2ed4f7426322bc0; _px3=77c5021a52d97ac8c402213db775910b130342d0acd4deab8078393d32463e69:qpxOFKUYYJzz/MEMQUlrQYvdynK/SDPqFzrTIun9LxGFA/PFFxR90GpnOEHmarDNZMuQ3Ge+0uozJ66P/xzccg==:1000:r9V+4HlVOuKmYqY0TVM8pjaOs3hgarkJ0vkXU5P+ZA0Vj81KBUOMBnVgWLqRzbEs6EE/LPNy3NJ9kVScWBpEOiBJ+vWVL34SsI5ThZklCn6Nm/P6hcU4aTOrKtuIFxvd3kXPgTE3/DJYxHpWk9JIVAJPJfGHuUxq4hhnw71WyiAm5q/C1rM0Q6DcY6PZzoPPpbBlLc909XzaekW6ho3nxg==; _px=qpxOFKUYYJzz/MEMQUlrQYvdynK/SDPqFzrTIun9LxGFA/PFFxR90GpnOEHmarDNZMuQ3Ge+0uozJ66P/xzccg==:1000:Y4pXjSzsOoZmu9BVlUiEqhRdjJZ0WKEPRWGgYjb0BWNRqrrHKYYgY1G+f91RiTmCFtmfaHTzIKgxGVz9wIlsvjA7zV3Nq+b0L6wi+/8tWVJRCe/D5g1Qr7fAaUzn9d9h/9BGgMcvh+jZjHmvTgQL3dYeXx2lxJLw+4dKRQxJ0C/x3obzqrT8nSXVZfX34llT3ePhjVSpo8afxzMLq3y4izWFkjVyQKtoeHqBUGNKV28fyBujMOuYAJEd5Z6I03W2vTlxSXTFOW9+RN5V+9sMBw==; s_pers=%20buFirstVisit%3Dcore%252Ccs%252Cothers%252Chelp%252Ctb%252Ccw%252Cmoney%7C1779113678163%3B%20gpv_v6%3Dno%2520value%7C1622382871339%3B; s_sess=%20buVisited%3Dcs%252Ccore%3B%20s_sq%3Dcheggincriovalidation%253D%252526pid%25253Dchegg%2525257Cweb%2525257Ccs%2525257Cchegg%25252520study%25252520homepage%252526pidt%25253D1%252526oid%25253Dfunctionqr%25252528%25252529%2525257B%2525257D%252526oidt%25253D2%252526ot%25253DDIV%3B%20s_ptc%3D%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D45D91C60C20A5CBD-1F362F14A572F674%3B; _gali=chegg-searchbox; AMCV_3FE7CBC1556605A77F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18778%7CMCMID%7C60185159885597638692678916017568026992%7CMCAAMLH-1622985881%7C3%7CMCAAMB-1622985881%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1622388281s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0%7CMCCIDH%7C-608999569',
    'origin':
    'https://www.chegg.com',
    'pragma':
    'no-cache',
    'referer':
    'https://www.chegg.com/',
    "sec-ch-ua-platform":
    "Windows",
    'sec-ch-ua':
    '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile':
    '?0',
    'sec-fetch-dest':
    'empty',
    'sec-fetch-mode':
    'cors',
    'sec-fetch-site':
    'same-site',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}
with open('./chegg_cookies.txt', 'r') as cookies:
    chegg_cookies = cookies.read().splitlines()
with open('./solCookie.txt', 'r') as cookies:
    sol_cookies = cookies.read().splitlines()


def HeaderGen():
    SelectedCookie = random.choice(sol_cookies)
    header = {
        'authority': 'www.chegg.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua':
        '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 11; SM-S134DL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36',
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        # Requests sorts cookies= alphabetically
        'cookie': f'{SelectedCookie}',
    }
    List = [SelectedCookie, header]
    return List


def newlikeIt(link, cookie):
    # print("HAM")
    # try:
    try:
        grabbedId = int(link.split('-')[-1].replace("q", ""))
    except:
        print("Invalid Chegg Link")
        return [403]
    headers = {
        'accept':
        '*/*',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'en-US,en;q=0.9',
        'apollographql-client-name':
        'chegg-web',
        'apollographql-client-version':
        'main-7d9be4fe-2517003393',
        'authorization':
        'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-length':
        '199',
        'content-type':
        'application/json',
        'cookie':
        'V=02c0fe8dc40d11810182bbfde45d001a62998285bd9074.26916316; userData=%7B%22authStatus%22%3A%22Logged%20Out%22%2C%22attributes%22%3A%7B%22uvn%22%3A%2202c0fe8dc40d11810182bbfde45d001a62998285bd9074.26916316%22%7D%7D; CVID=32b8e33f-5a2f-4161-aa72-e333d0077bab; local_fallback_mcid=92166456725833517713904657896796382204; s_ecid=MCMID|92166456725833517713904657896796382204; _omappvp=owm0cmm1MaT3ooQKXZ4Y75GARnUE8YipU8PdBQb0mRpLaW9iewQ1GKDxGLLIFwyD0zTzjM5SKt3iufdxNel0GsVSvF7ZFwAB; pxcts=d7ac3406-e2ee-11ec-9749-445778654969; _pxvid=d7ac282a-e2ee-11ec-9749-445778654969; _ga=GA1.2.1311531286.1654227609; sa-user-id=s%253A0-0f663318-900b-4d44-6b9c-7767bf6d8c79.m0eBNnr%252F9YfdgYfajvUH0opy3T%252BJcsg69m1PvFYa%252FHU; sa-user-id-v2=s%253A0-0f663318-900b-4d44-6b9c-7767bf6d8c79%2524ip%2524139.135.55.125.jyOziUjygXs7fC8heJmJ7H5fpnI%252BnE32FRF4YoCVRaA; _gcl_au=1.1.1390498571.1654227611; IR_gbd=chegg.com; _rdt_uuid=1654227616670.e7f1a4e3-8296-4d01-8a64-2299827d5976; _fbp=fb.1.1654227617726.571264924; _cs_c=0; _scid=2192d5f6-4f30-4a68-835f-b6ebff22aeb1; _tt_enable_cookie=1; _ttp=8127a3ef-d0bb-4604-9383-1ef87066a680; _sctr=1|1654196400000; _cs_cvars=%7B%221%22%3A%5B%22Page%20Name%22%2C%22chegg%20study%20homepage%22%5D%2C%223%22%3A%5B%22Page%20Type%22%2C%22landing%20page%22%5D%7D; _cs_id=c4e41d90-b8fc-aa62-90d3-9e88a9d3c531.1654227623.1.1654227623.1654227623.1.1688391623761; PHPSESSID=7ur602hbep0vi0j19ilq9emk6j; user_geo_location=%7B%22country_iso_code%22%3A%22PK%22%2C%22country_name%22%3A%22Pakistan%22%2C%22region%22%3A%22PB%22%2C%22region_full%22%3A%22Punjab%22%2C%22city_name%22%3A%22Bahawalpur%22%2C%22postal_code%22%3A%2263100%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ur-PK%22%5D%7D%7D; C=0; O=0; optimizelyEndUserId=oeu1654227698014r0.937677030025041; usprivacy=1YNY; OneTrustWPCCPAGoogleOptOut=false; __gads=ID=661d74b69970fd90:T=1654227700:S=ALNI_MZtzggzBxzgOxGA4jCaXqHs6pj8XA; forterToken=189a94684273490a8dc47dc0a9f44d88_1654227700364__UDF43_13ck; _vid_t=hEhME5sBC/nS6MWNNK3E2KUEErIYvnwbJXcWOAl0oBw0OyvZph3lFrdKNu2Kdo02kkln5oeKdL3YNQ==; DFID=web|aebHT76whGmrJS2U0cNn; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%20b6205c14-cc22-43f4-8995-f33f107ae13b%2C%20%22created_date%22%20%3D%3E%202022-06-03T03%3A41%3A57.156Z%20%5D; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImhlbnJ5a2FzYWRhQG91dGxvb2suY29tIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsInN1YiI6ImI2MjA1YzE0LWNjMjItNDNmNC04OTk1LWYzM2YxMDdhZTEzYiIsImF1ZCI6IkNIR0ciLCJpYXQiOjE2NTQyMjc3MzUsImV4cCI6MTY2OTc3OTczNSwicmVwYWNrZXJfaWQiOiJhcHcifQ.7HtQIGCOXs146CGcul11U3f5aP9e78yvUp9qRcBrfdw2lnKPgghU-DZ-ZaDHa7YrsW-0ETKhWwjBbOrO7gv8KSu-n7Vf7OfT4Cz-P_tvz_iQlwCAINe_xbLhG-p-nhbWnhwwsVFkmkUYkfN0IzZ7Jo0yijJdmCpfM-IcjqVzwlz4kzxppTl-C5ww21zn5ls1plrY8foAy2HH8qywSH5d9wMs056taNNNdR2H6bng62Y4-1pO5oA2ZIPcj18UinavWH6ZBbLehLFntvckH3Jg6GzyIfSdbGZFWPy2eoCgusfO5jeai0dJx3WHFaSZdcrpBIL8xi1QprQJ2FySsGTg_g; U=d04e4d85d7bc4d8f38bf528c549b1708; sourceTracking=google; _sdsat_cheggUserUUID=b6205c14-cc22-43f4-8995-f33f107ae13b; mcid=30728493361063577622717392572076184459; _gac_UA-499838-3=1.1654227742.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; _gcl_aw=GCL.1654227744.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; _gcl_dc=GCL.1654227744.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; chegg_web_cbr_qna_id=b75; exp=C026A%7CA560B%7CA127D; expkey=33708D223198904E27D1FB145FC6C46E; _pbjs_userid_consent_data=3524755945110770; _pubcid=463390be-7614-4879-86f2-848a6f9c788f; AMZN-Token=v2FweHxsS3NCM1pVNC9EV3pNVE9uWXJSSHdLRTM1QS9VVXluTnlXOEd0RHVQanliNG1JMnZ6RWpIeUpva1hMQjFiWmk5NHlpa0kweG9XUFVvdllsWkZrZ0h3dzV4WS9qOFNnU0UvS0grSDdzK1B2MENmSFF6Q2psaHpYcE9UQjA9Ymt2AWJpdnggNzcrOUF1Ky92ZSsvdlhJd1ZsUHZ2NzBJNzcrOVh3PT3/; b6205c14-cc22-43f4-8995-f33f107ae13b_TMXCookie=60; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%227a0fa1f2-33bc-4a43-98d9-6bfd78876e2d%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-05-03T03%3A46%3A52%22%7D; connectid=%7B%7D; _sdsat_authState=Soft%20Logged%20In; _lr_sampling_rate=100; intlPaQExitIntentModal=hide; ab.storage.deviceId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22bc3b744a-a04f-0916-d0b7-bb99d81b7b51%22%2C%22c%22%3A1654227740193%2C%22l%22%3A1654580861728%7D; ab.storage.userId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22b6205c14-cc22-43f4-8995-f33f107ae13b%22%2C%22c%22%3A1654227740175%2C%22l%22%3A1654580861732%7D; _lr_geo_location=PK; _gid=GA1.2.717477769.1654580873; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jun+07+2022+11%3A04%3A57+GMT%2B0500+(Pakistan+Standard+Time)&version=6.18.0&hosts=&consentId=2a8b2d7a-0c9d-4afb-86d1-8252153feb66&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; ab.storage.sessionId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22477d2dee-a3bd-ad13-e48a-2400fa6e297a%22%2C%22e%22%3A1654583697253%2C%22c%22%3A1654580861724%2C%22l%22%3A1654581897253%7D; _sdsat_highestContentConfidence={%22course_uuid%22:%2211f7ae34-5cbe-423b-b356-08ff5117fb79%22%2C%22course_name%22:%22c-programming-language%22%2C%22confidence%22:0.4237%2C%22year_in_school%22:%22college-year-1%22%2C%22subject%22:[{%22uuid%22:%226c009000-6a96-4469-88c3-1fbb987e41d0%22%2C%22name%22:%22computer-science%22}]}; _tq_id.TV-8145726354-1.ad8a=cf66e739ec7002ea.1654227614.0.1654581905..; IR_14422=1654581904846%7C0%7C1654581904846%7C%7C; _uetsid=5fc9e120e62511eca5963741d8d823d2; _uetvid=deeb3e20e2ee11ec881a9d222d1fa5eb; _px3=70bcfd04e43de741b5dd1d404c96ad6c989b92825532887cde032bdc91a106ea:uP0PsNnwMTCm/k7DTnRE9xyCpT9FG8Xy+Ft/T9VFJhsTrvk89rXt67AEae0lFajT3Q03L/DZj/DeQAQbjyNMtQ==:1000:kdmoJBZ4dliuofCHqAxcOcz06mxnZzYzMYuv0Eck/OG4aumjx8mHiDCJ6D3nWCQma4yf2LMpJ5KzD+RDST5eg2BXIL+fpL7C+h2jEGgvyH2GAs0uJnpM6mvwHKw9RVgyRWGqSuG2cw2kPxtruYyDZa1Bg2cBr/pDyuadn0JQ2Ln0/GjJVy0OVC0S5/pZk/T+nx0XJkeIq+2H65nSd+BELg==; _px=uP0PsNnwMTCm/k7DTnRE9xyCpT9FG8Xy+Ft/T9VFJhsTrvk89rXt67AEae0lFajT3Q03L/DZj/DeQAQbjyNMtQ==:1000:/jvbrpX2JQHDVpf8whrU0wsBPILLTIo3jAgO24BVSws+OutDYc3fqE9o/nnPJE5t/sSALgqm0IngBwjcHJhFngEKhMRrIwdYwbz3DqUwGoZQJwOnBBZFOmqoeVCgEtl3cIUak+IxsJkNzp7FbGo9tlKWRyiQtKcQ0QtfCerdwPQvAfSJ0rm1lx2Wssr2gFyiR0VzK/+VEykWHsxrPopeagb+G9Ayl6sAENw9YQsmZJyHWI+YCDsvKfsQaNuq34foyCOfbhYLau/c+0cYSc6LXg==; _clck=fbw7g7|1|f25|0; CSID=1654655331908; __gpi=UID=000008127be9f1ac:T=1654227700:RT=1654655331:S=ALNI_MYpps8Q4Rr0CKO73JNtEYBxfMLSPw; CSessionID=651e0c6a-267a-4b2a-b1a2-e1df342c62c8; SU=ftp5TnMKF48aQp9HKfL9AkaXsKnaNwon3q6q40oX5MIznIj4cZj6OCufOHQ8Dr0waL5Ac8P54gonZNMojl8EjztPqOpL1F7FNLnxvvyYwsuV9TvGBkKlThH-Tzdsn9FT; _clsk=19965qh|1654656295078|2|1|j.clarity.ms/collect',
        'origin':
        'https://www.chegg.com',
        'referer':
        'https://www.chegg.com/',
        'sec-ch-ua':
        '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-ch-ua-platform':
        '"Windows"',
        'sec-fetch-dest':
        'empty',
        'sec-fetch-mode':
        'cors',
        'sec-fetch-site':
        'same-site',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 11; SM-S134DL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36',
        # 'x-chegg-referrer': 'https://www.chegg.com/homework-help/questions-and-answers/1-grief-perceive--2-aware-ambiguous-loss-q92578455'
    }
    Answerquery = {
        "operationName": "QnaPageQuestionByLegacyId",
        "variables": {
            "id": grabbedId
        },
        "extensions": {
            "persistedQuery": {
                "version":
                1,
                "sha256Hash":
                "26efed323ef07d1759f67adadd2832ac85d7046b7eca681fe224d7824bab0928"
            }
        }
    }
    LegacyId = requests.post('https://gateway.chegg.com/one-graph/graphql',
                             headers=headers,
                             data=json.dumps(Answerquery))
    print(LegacyId.cookies.get_dict())
    json.dump(LegacyId.json(), open("SolutionJson.json", "w"), indent=4)
    LegacyId = LegacyId.json(
    )["data"]["questionByLegacyId"]["htmlAnswers"][0]["legacyId"]
    LikeQuery = {
        "operationName": "StoreUserContentReview",
        "variables": {
            "storeUserContentReviewInput": {
                "contentId": f"{LegacyId}",
                "contentReviewType": "LIKE_DISLIKE",
                "contentType": "ANSWER",
                "contentReviewValue": "LIKE",
                "contentReviewerDeviceType": "Web"
            }
        },
        "extensions": {
            "persistedQuery": {
                "version":
                1,
                "sha256Hash":
                "8ff728ee435482ff145899aa4bb94dad9e21d5bb0063c810b23b78403f58fb5e"
            }
        }
    }
    headers = {
        'cookie':
        cookie,
        'apollographql-client-name':
        'chegg-web',
        'apollographql-client-version':
        'main-7d9be4fe-2517003393',
        'authorization':
        'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 11; SM-S134DL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36',
    }
    responsed = requests.post('https://gateway.chegg.com/one-graph/graphql',
                              headers=headers,
                              data=json.dumps(LikeQuery))
    print(responsed.cookies.get_dict())
    ValueRet = responsed.json()["data"]["storeUserContentReview"]
    print(str(ValueRet))
    return [200]
    # except:
    # 	return [403]


def TBSHtmlGenerator(Answer, Question):
    Html = '''<html><head></head><body><div class="main">
	<h2 class="accordion active"><b>Question</b></h2>
								<div class="question">



	<div id="mobile-question-style" style="font-family: 'Helvetica Neue',Helvetica,Arial; color:#333333;">''' + '\n{}\n'.format(
        Question) + '''</div>


										</div>
								<h2 class="accordion active"><b>Answer</b></h2><div class="question">
										''' + '\n{}\n'.format(Answer) + '''</div>
				<script>
				var acc = document.getElementsByClassName("accordion");
				var i;
				for (i = 0; i < acc.length; i++) {
					acc[i].addEventListener("click", function () {
						this.nextElementSibling.classList.toggle('collapse')
						this.nextElementSibling.classList.toggle('expand')

					});
				}
			</script>
				<style>

			.img-container-block {
				text-align: center;
			}
			.img-container-inline {
				text-align: center;
				display: block;
			}
			.img-container img {
				width: 92px;
				position: absolute;
				left: 25%;
				top: 6px;
				border: 2px solid #00247;
				border-radius: 50px;
			}
			.step {
				margin: auto;
				margin-top: 7px;
				text-align: center;
				padding: 7px;
				color: #fff;
				font-size: 16px;
				background: #f78112;
				font-weight: bold;
				border-radius: 15px;
			}
			.accordion {
				background-color: #f78112;
				padding: 10px;
				font-size: 15px;
				color: white;
				border-radius: 29px;
				text-align: center;
				text-transform: uppercase;
				width: auto;
				height: auto;
				overflow: hidden;
				filter: brightness(100%);
				transition: filter 0.15s;
			}
	.ad_shadow{
				box-shadow: 0px 0px 3px 1px rgba(0,0,0,0.75);
				-webkit-box-shadow: 0px 0px 3px 1px rgba(0,0,0,0.75);
				-moz-box-shadow: 0px 0px 3px 1px rgba(0,0,0,0.75);

			}
	.ad{
				width: 18%;
				margin-right: 9px;
				border-radius: 10px;
				max-height: 92px;
			}
	.products{
		margin:10px 0px 10px 19px;
	}
			.question {
				padding: 0 10px;
				margin: 0px 35px 0px 35px;
				border-left: 12px solid;
				border-radius: 20px;
				border-top: 2px solid;
				border-right: 12px solid;
				border-bottom: 2px solid;
				border-color: #f78112;
				text-align: center;
				overflow: hidden;
			}
			.main {
				background-color: white;
			}
			</style></div></body></html>'''
    return Html


def TBS(Question, Cookie, Link):
    try:
        ChapterId = Question.split('"chapterId":"')[1].split('"')[0]
    except:
        ChapterId = Question.split("\\/?id=")[1].split('&')[0]
    try:
        likes = Question.split('"positiveReviewCount":')[1].split(',')[0]
    except:
        likes = "0"
    try:
        dislikes = Question.split('"negativeReviewCount":')[1].split('}')[0]
    except:
        dislikes = "0"
    Token = str(Question.split('"token":"')[1].split('"')[0])
    ISBN = str(Question.split('"isbn13":"')[1].split('"')[0])
    QID = str(Question.split('problemId":"')[1].split('"')[0])
    try:
        cheggheader = {
            'accept':
            'application/json',
            'accept-encoding':
            'gzip, deflate, br',
            'accept-language':
            'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type':
            'application/json',
            'cookie':
            "{}".format(Cookie),
            'origin':
            'https://www.chegg.com',
            'referer':
            "{}".format(Link),
            'sec-fetch-dest':
            'empty',
            'sec-fetch-mode':
            'cors',
            'sec-fetch-site':
            'same-origin',
            'user-agent':
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36',
        }
        query = {
            "query": {
                "operationName": "getSolutionDetails",
                "variables": {
                    "isbn13": "{}".format(ISBN),
                    "chapterId": "{}".format(ChapterId),
                    "problemId": "{}".format(QID)
                }
            },
            "token": "{}".format(Token)
        }
        Content = requests.post(
            'https://www.chegg.com/study/_ajax/persistquerygraphql',
            headers=cheggheader,
            data=json.dumps(query))
        json.dump(Content.json(), open("tbsSolution.json", "w"), indent=4)
        Content = Content.text.replace("\\", "")
        totalSteps = Content.split('"totalSteps":')[1].split(',')[0]
        book = Content.split('"coverName":"')[1].split('"')[0]
        edition = Content.split('"editionNumber":')[1].split(',')[0]
        bookmarks = Content.split('"userAssetCount":')[1].split(',')[0]
        chapterName = Content.split('chapterName":"')[1].split('"')[0]
        problemName = Content.split('problemName":"')[1].split('"')[0]
        try:
            Question = Content.split('problemHtml":"')[1].split('","user')[0]
        except:
            Question = ''
        HTMlIndexes = Content.split('"html":"')
        HTMlIndexes[0] = ''
        count = 0
        Steps = ''
        for i in HTMlIndexes:
            if '<div' in i:
                count += 1
                Steps += f'''<li><section class="step TBS_SOLUTION_STEP opened" data-id="9.1-2lo-2"><h4 class="step-header" tabindex="0" role="button" aria-pressed="true"><span class="step-num">Step {count} </span><span class="step-total">of {totalSteps}</span></h4><div class="content"><div class="html step-html">{i.split('","link"')[0]}</div></section></li>'''
    except:
        Steps = '<p><span style="background-color: #ffffff; color: #ff0000; font-size: 18px;"><strong>Oh No!! No One Has Answered It Yet...</strong></span></p>'
    return {
        "solution":
        Steps.replace('class="content"', 'class="tbs_content"'),
        "question":
        Question,
        "likes":
        likes,
        "dislikes":
        dislikes,
        "type":
        "tbs",
        "about":
        f"bookmarks={bookmarks},bookName={book},editionNumber={edition},chapter={chapterName},problem={problemName}"
    }


def QuestionHtml(Extracted, q1):
    totalAnswers = ""
    try:
        Question = str(
            Extracted[Extracted.
                      index('<div class="ugc-base question-body-text">'):])
        Question = Question[:Question.index('<div class="avatar-comments')]
        Question = Question[:Question.rfind('</div>')] + "</div>"
        Question = Question.replace('"//', '"https://')
        Question = Question.replace('<img ', '<img class="Beaster" ')
        try:
            answerer = Extracted.split('"displayName":"')[1].split('"')[0]
        except:
            answerer = "Anonymous"
        totalAnswers = Extracted.split(
            "<span class='answers-total'>")[1].split('<')[0]
    except:
        Question = '<p><span style="color: #ff0000;text-align: center;display: block;"><strong>No one has Answered it yet</strong></span></p>'
    q1.put([totalAnswers, answerer, Question])


def CommentsHtml(Extracted, q3):
    try:
        Comment = Extracted.split(
            '<div class="comments-markup mod-parent-container">')
        Comment[-1] = Comment[-1].split('<div class="leave-comment ">')[0]
        Comments = ''
        for i in Comment:
            if '<span class="comment-date">' in i:
                Comments += (
                    '<div class="comments-markup mod-parent-container">' + i)
        Comments = Comments.replace('"//', '"https://')
        if Comments == '':
            Comments = '<p><span style="color: #ff0000;text-align: center;display: block;"><strong>No one has commented it yet</strong></span></p>'
    except:
        Comments = '<p><span style="color: #ff0000;text-align: center;display: block;"><strong>No Comments</strong></span></p>'
    q3.put(Comments)


def Like_Dislike(Extracted, header, q4):
    Likes = '0'
    Dislikes = '0'
    try:
        LikID = Extracted.split('"answerId":')[1].split(',')[0]
    except:
        try:
            LikID = Extracted.split('data-answerId="')[1].split('"')[0]
        except:
            LikID = 'None'
    Like_disLike = requests.get(
        'https://www.chegg.com/study/_ajax/contentfeedback/getreview?entityType=ANSWER&entityId={}'
        .format(LikID),
        headers=header).text
    if LikID != 'None':
        for i in Like_disLike.split('}},'):
            try:
                Extract = i.split('"result":')[1]
                if len(Extract) > 10:
                    for under in Extract.split('"}'):
                        if '"reviewValue":"0' in under:
                            Likes = under.split('"count":')[1].split(',')[0]
                        elif '"reviewValue":"1' in under:
                            Dislikes = under.split('"count":')[1].split(',')[0]
            except:
                Likes = '0'
                Dislikes = '0'
    q4.put([Likes, Dislikes])


def QASolution(Extracted, q5):
    try:
        Extracted = str(
            Extracted[Extracted.
                      index('<div class="answer-given-body ugc-base">'):])
        Solution = str(Extracted[:Extracted.index('<a href="#"')])
        Solution = Solution.replace('"//', '"https://')
        Solution = Solution.replace('<img', '<img class="Beaster"')
    except:
        Solution = "<p><span style='color: #339966;'><strong>This question hasn't been answered yet!</strong></span></p>"
    q5.put(Solution)


def solution(Extracted, header):
    open("Died.html", "w", encoding="utf-8").write(Extracted)
    Threads = []
    q1 = queue.Queue()
    q3 = queue.Queue()
    q4 = queue.Queue()
    q5 = queue.Queue()
    Threads.append(threading.Thread(target=QuestionHtml, args=(Extracted, q1)))
    Threads.append(threading.Thread(target=CommentsHtml, args=(Extracted, q3)))
    Threads.append(
        threading.Thread(target=Like_Dislike, args=(Extracted, header, q4)))
    Threads.append(threading.Thread(target=QASolution, args=(Extracted, q5)))
    for i in Threads:
        i.start()
    try:
        QuestionHead = '<em>' + \
         Extracted.split('headline"><em>')[1].split('</h1>')[0]
    except:
        QuestionHead = '<b>Question</b>'
    for i in Threads:
        i.join()
    totalAns, Answerer, Question = q1.get()
    Comments = q3.get()
    Likes, Dislikes = q4.get()
    Solution = q5.get()
    finalJson = {
        "type": "qa",
        "solution": Solution.replace("'", '"'),
        "question": Question.replace("'", '"'),
        "likes": Likes,
        "dislikes": Dislikes,
        "comments": Comments,
        "questionHead": QuestionHead,
        "expert": Answerer,
        "expertAns": totalAns
    }
    return finalJson


def ContentGrabber(url):
    Cookie, header = HeaderGen()
    Responce = requests.get(url, headers=header)
    return ([Cookie, header, Responce])


def grb_det(url):
    # try:
    # 	headers = {
    # 			'authority': 'atc-edge.studybreakmedia.com',
    # 			'pragma': 'no-cache',
    # 			'cache-control': 'no-cache',
    # 			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    # 			'sec-ch-ua-mobile': '?0',
    # 					'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    # 					'sec-ch-ua-platform': '"Windows"',
    # 					'accept': '*/*',
    # 					'sec-fetch-site': 'cross-site',
    # 					'sec-fetch-mode': 'no-cors',
    # 					'sec-fetch-dest': 'script',
    # 					'referer': f'{url}',
    # 					'cookie': random.choice(chegg_cookies),
    # 					'accept-language': 'en-US,en;q=0.9',
    # 		}
    # 	response = requests.get(url, headers=headers).text
    # 	open("new9111.html", "w").write(response)
    # 	question_head = response.split('<em>Question: </em>')[1].split('</h1>')[
    # 			0].replace('\\n', ' ').replace('<br>', '')
    # 	subjectName = response.split('"subSubjectName":"')[1].split('"')[0]
    # 	try:
    # 		positiveRat = response.split('"positiveAnswerReviewCount"')[
    # 			1].split('"')[0]
    # 	except:
    # 		positiveRat = "0"
    # 	try:
    # 		NegRat = response.split('"negativeAnswerReviewCount"')[
    # 			1].split('"')[0]
    # 	except:
    # 		NegRat = "0"
    # 	resp = {"code": "1", "positive": positiveRat, "negative": NegRat,
    # 				"queHead": question_head, "subjectName": subjectName}
    # 	return resp
    # except:
    # 	return {"code": "303", "text": "Invalid Chegg Link"}
    resp = {
        "code": "1",
        "positive": "0",
        "negative": "0",
        "queHead":
        "This process can take upto 4 minutes max, wait until you get success.",
        "subjectName": "None"
    }
    return resp


def SolutionFinalizer(Extracted, header, Cookie, url):
    if 'TBS' in Extracted.split('"pageName":"')[1].split('"')[0]:
        data = TBS(Extracted, Cookie, url)
    else:
        data = solution(Extracted, header)
    return (data)


def newSolutionApi(grabbedId):
    headers = {
        'accept':
        '*/*',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'en-US,en;q=0.9',
        'apollographql-client-name':
        'chegg-web',
        'apollographql-client-version':
        'main-7d9be4fe-2517003393',
        'authorization':
        'Basic TnNZS3dJMGxMdVhBQWQwenFTMHFlak5UVXAwb1l1WDY6R09JZVdFRnVvNndRRFZ4Ug==',
        'content-length':
        '199',
        'content-type':
        'application/json',
        'cookie':
        'V=02c0fe8dc40d11810182bbfde45d001a62998285bd9074.26916316; userData=%7B%22authStatus%22%3A%22Logged%20Out%22%2C%22attributes%22%3A%7B%22uvn%22%3A%2202c0fe8dc40d11810182bbfde45d001a62998285bd9074.26916316%22%7D%7D; CVID=32b8e33f-5a2f-4161-aa72-e333d0077bab; local_fallback_mcid=92166456725833517713904657896796382204; s_ecid=MCMID|92166456725833517713904657896796382204; _omappvp=owm0cmm1MaT3ooQKXZ4Y75GARnUE8YipU8PdBQb0mRpLaW9iewQ1GKDxGLLIFwyD0zTzjM5SKt3iufdxNel0GsVSvF7ZFwAB; pxcts=d7ac3406-e2ee-11ec-9749-445778654969; _pxvid=d7ac282a-e2ee-11ec-9749-445778654969; _ga=GA1.2.1311531286.1654227609; sa-user-id=s%253A0-0f663318-900b-4d44-6b9c-7767bf6d8c79.m0eBNnr%252F9YfdgYfajvUH0opy3T%252BJcsg69m1PvFYa%252FHU; sa-user-id-v2=s%253A0-0f663318-900b-4d44-6b9c-7767bf6d8c79%2524ip%2524139.135.55.125.jyOziUjygXs7fC8heJmJ7H5fpnI%252BnE32FRF4YoCVRaA; _gcl_au=1.1.1390498571.1654227611; IR_gbd=chegg.com; _rdt_uuid=1654227616670.e7f1a4e3-8296-4d01-8a64-2299827d5976; _fbp=fb.1.1654227617726.571264924; _cs_c=0; _scid=2192d5f6-4f30-4a68-835f-b6ebff22aeb1; _tt_enable_cookie=1; _ttp=8127a3ef-d0bb-4604-9383-1ef87066a680; _sctr=1|1654196400000; _cs_cvars=%7B%221%22%3A%5B%22Page%20Name%22%2C%22chegg%20study%20homepage%22%5D%2C%223%22%3A%5B%22Page%20Type%22%2C%22landing%20page%22%5D%7D; _cs_id=c4e41d90-b8fc-aa62-90d3-9e88a9d3c531.1654227623.1.1654227623.1654227623.1.1688391623761; PHPSESSID=7ur602hbep0vi0j19ilq9emk6j; user_geo_location=%7B%22country_iso_code%22%3A%22PK%22%2C%22country_name%22%3A%22Pakistan%22%2C%22region%22%3A%22PB%22%2C%22region_full%22%3A%22Punjab%22%2C%22city_name%22%3A%22Bahawalpur%22%2C%22postal_code%22%3A%2263100%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ur-PK%22%5D%7D%7D; C=0; O=0; optimizelyEndUserId=oeu1654227698014r0.937677030025041; usprivacy=1YNY; OneTrustWPCCPAGoogleOptOut=false; __gads=ID=661d74b69970fd90:T=1654227700:S=ALNI_MZtzggzBxzgOxGA4jCaXqHs6pj8XA; forterToken=189a94684273490a8dc47dc0a9f44d88_1654227700364__UDF43_13ck; _vid_t=hEhME5sBC/nS6MWNNK3E2KUEErIYvnwbJXcWOAl0oBw0OyvZph3lFrdKNu2Kdo02kkln5oeKdL3YNQ==; DFID=web|aebHT76whGmrJS2U0cNn; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%20b6205c14-cc22-43f4-8995-f33f107ae13b%2C%20%22created_date%22%20%3D%3E%202022-06-03T03%3A41%3A57.156Z%20%5D; id_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImhlbnJ5a2FzYWRhQG91dGxvb2suY29tIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsInN1YiI6ImI2MjA1YzE0LWNjMjItNDNmNC04OTk1LWYzM2YxMDdhZTEzYiIsImF1ZCI6IkNIR0ciLCJpYXQiOjE2NTQyMjc3MzUsImV4cCI6MTY2OTc3OTczNSwicmVwYWNrZXJfaWQiOiJhcHcifQ.7HtQIGCOXs146CGcul11U3f5aP9e78yvUp9qRcBrfdw2lnKPgghU-DZ-ZaDHa7YrsW-0ETKhWwjBbOrO7gv8KSu-n7Vf7OfT4Cz-P_tvz_iQlwCAINe_xbLhG-p-nhbWnhwwsVFkmkUYkfN0IzZ7Jo0yijJdmCpfM-IcjqVzwlz4kzxppTl-C5ww21zn5ls1plrY8foAy2HH8qywSH5d9wMs056taNNNdR2H6bng62Y4-1pO5oA2ZIPcj18UinavWH6ZBbLehLFntvckH3Jg6GzyIfSdbGZFWPy2eoCgusfO5jeai0dJx3WHFaSZdcrpBIL8xi1QprQJ2FySsGTg_g; U=d04e4d85d7bc4d8f38bf528c549b1708; sourceTracking=google; _sdsat_cheggUserUUID=b6205c14-cc22-43f4-8995-f33f107ae13b; mcid=30728493361063577622717392572076184459; _gac_UA-499838-3=1.1654227742.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; _gcl_aw=GCL.1654227744.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; _gcl_dc=GCL.1654227744.EAIaIQobChMIuPr3_a2Q-AIVTdnVCh2faA0kEAAYASAAEgIco_D_BwE; chegg_web_cbr_qna_id=b75; exp=C026A%7CA560B%7CA127D; expkey=33708D223198904E27D1FB145FC6C46E; _pbjs_userid_consent_data=3524755945110770; _pubcid=463390be-7614-4879-86f2-848a6f9c788f; AMZN-Token=v2FweHxsS3NCM1pVNC9EV3pNVE9uWXJSSHdLRTM1QS9VVXluTnlXOEd0RHVQanliNG1JMnZ6RWpIeUpva1hMQjFiWmk5NHlpa0kweG9XUFVvdllsWkZrZ0h3dzV4WS9qOFNnU0UvS0grSDdzK1B2MENmSFF6Q2psaHpYcE9UQjA9Ymt2AWJpdnggNzcrOUF1Ky92ZSsvdlhJd1ZsUHZ2NzBJNzcrOVh3PT3/; b6205c14-cc22-43f4-8995-f33f107ae13b_TMXCookie=60; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%227a0fa1f2-33bc-4a43-98d9-6bfd78876e2d%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-05-03T03%3A46%3A52%22%7D; connectid=%7B%7D; _sdsat_authState=Soft%20Logged%20In; _lr_sampling_rate=100; intlPaQExitIntentModal=hide; ab.storage.deviceId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22bc3b744a-a04f-0916-d0b7-bb99d81b7b51%22%2C%22c%22%3A1654227740193%2C%22l%22%3A1654580861728%7D; ab.storage.userId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22b6205c14-cc22-43f4-8995-f33f107ae13b%22%2C%22c%22%3A1654227740175%2C%22l%22%3A1654580861732%7D; _lr_geo_location=PK; _gid=GA1.2.717477769.1654580873; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jun+07+2022+11%3A04%3A57+GMT%2B0500+(Pakistan+Standard+Time)&version=6.18.0&hosts=&consentId=2a8b2d7a-0c9d-4afb-86d1-8252153feb66&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; ab.storage.sessionId.b283d3f6-78a7-451c-8b93-d98cdb32f9f1=%7B%22g%22%3A%22477d2dee-a3bd-ad13-e48a-2400fa6e297a%22%2C%22e%22%3A1654583697253%2C%22c%22%3A1654580861724%2C%22l%22%3A1654581897253%7D; _sdsat_highestContentConfidence={%22course_uuid%22:%2211f7ae34-5cbe-423b-b356-08ff5117fb79%22%2C%22course_name%22:%22c-programming-language%22%2C%22confidence%22:0.4237%2C%22year_in_school%22:%22college-year-1%22%2C%22subject%22:[{%22uuid%22:%226c009000-6a96-4469-88c3-1fbb987e41d0%22%2C%22name%22:%22computer-science%22}]}; _tq_id.TV-8145726354-1.ad8a=cf66e739ec7002ea.1654227614.0.1654581905..; IR_14422=1654581904846%7C0%7C1654581904846%7C%7C; _uetsid=5fc9e120e62511eca5963741d8d823d2; _uetvid=deeb3e20e2ee11ec881a9d222d1fa5eb; _px3=70bcfd04e43de741b5dd1d404c96ad6c989b92825532887cde032bdc91a106ea:uP0PsNnwMTCm/k7DTnRE9xyCpT9FG8Xy+Ft/T9VFJhsTrvk89rXt67AEae0lFajT3Q03L/DZj/DeQAQbjyNMtQ==:1000:kdmoJBZ4dliuofCHqAxcOcz06mxnZzYzMYuv0Eck/OG4aumjx8mHiDCJ6D3nWCQma4yf2LMpJ5KzD+RDST5eg2BXIL+fpL7C+h2jEGgvyH2GAs0uJnpM6mvwHKw9RVgyRWGqSuG2cw2kPxtruYyDZa1Bg2cBr/pDyuadn0JQ2Ln0/GjJVy0OVC0S5/pZk/T+nx0XJkeIq+2H65nSd+BELg==; _px=uP0PsNnwMTCm/k7DTnRE9xyCpT9FG8Xy+Ft/T9VFJhsTrvk89rXt67AEae0lFajT3Q03L/DZj/DeQAQbjyNMtQ==:1000:/jvbrpX2JQHDVpf8whrU0wsBPILLTIo3jAgO24BVSws+OutDYc3fqE9o/nnPJE5t/sSALgqm0IngBwjcHJhFngEKhMRrIwdYwbz3DqUwGoZQJwOnBBZFOmqoeVCgEtl3cIUak+IxsJkNzp7FbGo9tlKWRyiQtKcQ0QtfCerdwPQvAfSJ0rm1lx2Wssr2gFyiR0VzK/+VEykWHsxrPopeagb+G9Ayl6sAENw9YQsmZJyHWI+YCDsvKfsQaNuq34foyCOfbhYLau/c+0cYSc6LXg==; _clck=fbw7g7|1|f25|0; CSID=1654655331908; __gpi=UID=000008127be9f1ac:T=1654227700:RT=1654655331:S=ALNI_MYpps8Q4Rr0CKO73JNtEYBxfMLSPw; CSessionID=651e0c6a-267a-4b2a-b1a2-e1df342c62c8; SU=ftp5TnMKF48aQp9HKfL9AkaXsKnaNwon3q6q40oX5MIznIj4cZj6OCufOHQ8Dr0waL5Ac8P54gonZNMojl8EjztPqOpL1F7FNLnxvvyYwsuV9TvGBkKlThH-Tzdsn9FT; _clsk=19965qh|1654656295078|2|1|j.clarity.ms/collect',
        'origin':
        'https://www.chegg.com',
        'referer':
        'https://www.chegg.com/',
        'sec-ch-ua':
        '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-ch-ua-platform':
        '"Windows"',
        'sec-fetch-dest':
        'empty',
        'sec-fetch-mode':
        'cors',
        'sec-fetch-site':
        'same-site',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 11; SM-S134DL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36',
        # 'x-chegg-referrer': 'https://www.chegg.com/homework-help/questions-and-answers/1-grief-perceive--2-aware-ambiguous-loss-q92578455'
    }
    Answerquery = {
        "operationName": "QnaPageQuestionByLegacyId",
        "variables": {
            "id": grabbedId
        },
        "extensions": {
            "persistedQuery": {
                "version":
                1,
                "sha256Hash":
                "26efed323ef07d1759f67adadd2832ac85d7046b7eca681fe224d7824bab0928"
            }
        }
    }
    LegacyId = requests.post('https://gateway.chegg.com/one-graph/graphql',
                             headers=headers,
                             data=json.dumps(Answerquery))
    return LegacyId


def likeIt(link):
    selec_cookie = random.choice(chegg_cookies)
    header = {
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language':
        'en-US,en;q=0.9',
        'content-type':
        "application/x-www-form-urlencoded; charset = UTF-8",
        'cookie':
        selec_cookie,
        'sec-ch-ua':
        '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-fetch-dest':
        'document',
        "sec-ch-ua-platform":
        "Windows",
        'sec-fetch-mode':
        'navigate',
        'sec-fetch-site':
        'none',
        'sec-fetch-user':
        '?1',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36'
    }
    content = requests.get(link, headers=header).text
    askerId = content.split('data-askerId="')[1].split('"')[0]
    entityId = content.split('data-answerId="')[1].split('"')[0]
    header['accept'] = 'application/json, text/javascript, */*q = 0.01'
    answerDate = content.split('data-ansCreateDate="')[1].split(
        '"')[0].replace(':', '%3A')
    questionId = content.split('data-qid="')[1].split('"')[0]
    token = content.split('"token":"')[1].split('"')[0]
    query = 'askerId={}&entityType=ANSWER&entityId={}&reviewType=LIKE_DISLIKE&reviewValue=0&answerCreatedDate={}&token={}&questionId={}'.format(
        askerId, entityId, answerDate, token, questionId)
    try:
        liked = requests.post(
            'https://www.chegg.com/study/_ajax/contentfeedback/savereview',
            headers=header,
            data=query).json()['httpCode']
        return liked
    except:
        return 400


@app.route("/")
def new():
    return "This is the main Page"


@app.route("/v1/unlock", methods=['GET', 'POST'])
def chegg_v1():
    data = request.get_json()
    grabbedId = int(data['url'].split('-')[-1].replace("q", ""))
    Content = newSolutionApi(grabbedId)
    mainData = Content.json()["data"]["questionByLegacyId"]
    Solution = mainData["htmlAnswers"][0]["answerData"]["html"]
    Question = mainData["content"]["body"]
    Answerer = mainData["htmlAnswers"][0]["answerData"]["author"]["firstName"]
    if (Answerer == None or Answerer.length < 4):
        Answerer = "Anonymous"
    Likes = "0"
    totalAns = mainData["htmlAnswers"][0]["answerData"]["author"][
        "answerCount"]
    Dislikes = "0"
    finalJson = {
        "type": "qa",
        "solution": Solution.replace("'", '"'),
        "question": Question.replace("'", '"'),
        "likes": Likes,
        "dislikes": Dislikes,
        "comments": "",
        "questionHead": "Expert Q&A",
        "expert": Answerer,
        "expertAns": totalAns
    }
    # Cookie, header, Responce = ContentGrabber(data["url"])
    # Extracted = Responce.text
    # solution = SolutionFinalizer(Extracted, header, Cookie, data["url"])
    print(finalJson)
    return finalJson


@app.route("/check")
def check():
    return render_template("new911.html")


@app.route("/v1/grab-sol", methods=['GET', 'POST'])
def grabSOl():
    data = request.get_json()
    try:
        grabbedId = int(data['url'].split('-')[-1].replace("q", ""))
        if "/homework-help/" not in data['url']:
            print("CHECK Completed")
            return jsonify(code="301",
                           text="Text Book Solutions not supported yet")
    except:
        print("Invalid Chegg Link")
        return jsonify(code="301", text="This question hasn't been solved yet")
    LegacyId = newSolutionApi(grabbedId)
    uuid = LegacyId.json()["data"]["questionByLegacyId"]["uuid"]
    mainData = LegacyId.json()["data"]["questionByLegacyId"]
    Solution = mainData["htmlAnswers"][0]["answerData"]["html"]
    Question = mainData["content"]["body"]
    Answerer = mainData["htmlAnswers"][0]["answerData"]["author"]["firstName"]
    if (Answerer == None or Answerer.length < 4):
        Answerer = "Anonymous"
    Likes = "0"
    totalAns = mainData["htmlAnswers"][0]["answerData"]["author"][
        "answerCount"]
    Dislikes = "0"
    finalJson = {
        "type": "qa",
        "solution": Solution.replace("'", '"'),
        "question": Question.replace("'", '"'),
        "likes": Likes,
        "dislikes": Dislikes,
        "comments": "",
        "questionHead": "Expert Q&A",
        "expert": Answerer,
        "expertAns": totalAns
    }
    text_Resp = LegacyId.text
    open("response.html", "w", encoding="utf-8").write(text_Resp)
    if int(LegacyId.status_code) == 403:
        return jsonify(code="301", text="Server is down, Try again later.")
    elif '"answeredStatus":"None"' in text_Resp:
        return jsonify(code="301", text="This question hasn't been solved yet")
    # elif 'TBS' in text_Resp.split('"pageName":"')[1].split('"')[0]:
    #     typeOfSol = "textbook"
    # else:
    typeOfSol = "qa"
    # try:
    #     uuid = text_Resp.split('"pageNameDetailed":"')[1].split('"')[0]
    # except:
    #     try:
    #         uuid = text_Resp.split('"questionUuid":"')[1].split('"')[0]
    #     except:
    #         try:
    #             uuid = text_Resp.split('"uuid":"')[1].split('"')[0]
    #         except:
    #             uuid = text_Resp.split('"questionId":')[1].split(',')[0]
    return jsonify(code="200",
                   uuid=uuid,
                   type=typeOfSol,
                   solution=Solution.replace("'", '"'),
                   question=Question.replace("'", '"'),
                   likes=Likes,
                   dislikes=Dislikes,
                   comments="",
                   questionHead="Expert Q&A",
                   expert=Answerer,
                   expertAns=totalAns)


@app.route("/v1/upvote", methods=['GET', 'POST'])
def upvote():
    data = request.get_json()
    state = data["state"]
    if state == 0 or state == "0":
        ups = int(data["do"])
        new_cookies = data["cookies"]
        print(f"Doing Likes: {ups}")
        done = []
        done_uuids = []
        count = 0
        crisp = 0
        while count < int(ups):
            while True:
                cookie = random.choice(new_cookies)
                if cookie not in done:
                    break
            # try:
            response = newlikeIt(data["url"], cookie)
            if response[0] == 200:
                count += 1
                crisp = 0
                print(
                    f"\033[1;32m Cookie Selected: {new_cookies.index(cookie)} | Like Status: Success"
                )
            else:
                if crisp == 4:
                    break
                else:
                    crisp += 1
                print(
                    f"\033[1;31m Cookie Selected: {new_cookies.index(cookie)} | Like Status: Failed"
                )
            done.append(cookie)
            done_uuids.append(cookie.split("PHPSESSID=")[1].split(";")[0])
            # except:
            # 	pass
            time.sleep(random.randint(3, 5))
        return jsonify(code="100", added=count, uuids=done_uuids)
    else:
        resp = grb_det(data["url"])
    if resp["code"] == "303":
        return resp
    return jsonify(data=resp, code="1")


app.run(host="0.0.0.0", port=0000)
