# get_friends_vk_api
A program that receives data about your friends such as: "First name, last name, country, city, birthday, gender" and saves them to such file formats as: "json, csv, tsv"

To get started, we will need to get an access token, and the ID of the client for whom we are making a report, to do this, click on this link

https://oauth.vk.com/authorize?client_id=51708572&display=page&redirect_uri=https://oauth.vk.com//blank.html&scope=offline,friends&response_type=token&v=5.131

after clicking on the link, you are asked to log in to your account
![Снимок экрана 2023-07-23 013938](https://github.com/Evafag02/get_friends_vk_api/assets/82770251/398c01ad-6114-4bb1-8414-9709451f2af4)

After that, you will be shown such a screen: 
![image](https://github.com/Evafag02/get_friends_vk_api/assets/82770251/7687c846-e7c4-4847-812d-41a83161ef25)

in the url output line, you will be shown a similar inscription:

https://oauth.vk.com/blank.html#access_token=vk1.a.1O6bSmpQ2wa7Vfr7sDEwNgof6SyuypbiCwalJ3ilk8zGQCqv38a5TBzFtkJxKHX3DqnMAW5lJDhegMmo88vSoJcoySQUHeMFSK8LgLSRlPsPP61S9yP8MJAWaS_iisrO9-MEpdUwHC935J_BpUlKggu-rOOcMLi0DZxcm3VerhZ4vXv0WYr01OmPjAVItPGJ2dPo1h_8WiRP4kduo3zzDQ&expires_in=0&user_id=547257989

we will need the part after "access_token=" before "&expires...", this will be our token, and we will also need the user_id, these are the numbers: 547257989
after that, we save the token to a file token.txt:

![Снимок экрана 2023-07-23 014654](https://github.com/Evafag02/get_friends_vk_api/assets/82770251/f9ced778-1e9c-4709-beb6-0d30c6fa1664)

next, open the command line (in windows 10, this is done by pressing win + r, and then in the window that opens, we enter cmd and press enter)
also, to work, we will need to download the requests library, this is done simply by entering the command line: 'pip install requests'

then open our file in the command line: "python <Path to file> <Path to token> <user_id> /optional/ --format (csv, tsv, json | default=cvs) --output (file name | default = 'report')"

if everything works correctly, you will get a message that everything has worked successfully
