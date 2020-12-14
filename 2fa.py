import smtplib
import csv
import random
import datetime
#### I have used bottom up design so easiest to start reading from the bottom #####

class Otp:
    def __init__(self, user_info, one_time):
        self.user_info = user_info
        self.one_time = str(one_time)

#### With assistance from https://automatetheboringstuff.com/chapter16/
    def send_mail(self):
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login('2fa.authenticator@gmail.com','Passwrd1987')
        s.sendmail('2fa.authenticator@gmail.com', (self.user_info) , 'Subject: App 2fa Code\n' +(self.one_time))
        s.close() 

###### GENERATES A ONE TIME PASSWORD ######
def generate_otp():
    random_num = random.randint(100000,999999)
    return random_num

def enter_opt(users, first, last):
    send_otp = generate_otp()
    v = Otp(users, send_otp)
    v.send_mail()
    try:
        while send_otp != int(input("Enter your one time password: ")):
            print('The number you entered is incorrect, send again?')
            otp_confirm = input('(y) for Yes (n) for No')
            if otp_confirm == 'y':
                return enter_opt(users, first, last)
            else: exit()     
        print('Log in successful')
        print('Welcome ' + first + ' ' + last + ' the time is {}'.format(datetime.datetime.now().time()))

    except ValueError :
        print('You must enter a numerical value, sending new one time code')
        return enter_opt(users, first,last)
    
   

########### ENCRYPTS / DECRYPTS INTO ASCII FORMAT THEN USES CALCULATION FOR FURTHER ENCRYPTION  #########
# ##### Side note, pretty proud of this part as i havnt been overly confident with class      
class Encryption:
    def __init__ (self, password):
        self.password=password

    def decrypt(self):
        
        decrypt_string = ''
        for i in self.password:
            i = i/12 * 4
            i = chr(int(i))
            decrypt_string += i
        return decrypt_string                     
                
    def encrypt(self):
        encrypt_list = []
        for i in self.password:
            i = ord(i)/4*12
            encrypt_list.append(int(i))
        return encrypt_list

###### PROMPTS USER TO LOGIN, CHECKS PASSWORD AGAINST THAT SAVED IN CSV FILE, SENDS USER_NAME ON TO CREATE OTP ####
def login():
    
    print('*********Welcome, Please Sign In********')
    user_name = input('Enter your user name: ')
    with open('user_log.csv', 'r') as temp:
        read_file = csv.DictReader(temp)
        """" I had a lot of trouble with this section as i kept on trying to use an else statement if 
            the user was not found, so it kept on iterating over each item and not finding it,
            i then went for the flag option to register if an email was found"""
        flag = 0
        for line in read_file:
            if user_name in line['email']:
                first, last = line['first_name'], line['last_name']
                flag += 1
        if flag == 0:
            print('User name not in database')
            return first_screen()
    ##### Allow users 3 attempts to login try_count (-) 1 per attempt ####
    try_count = 2
    while try_count >= 0:        
        with open('user_log.csv', 'r') as file:
            read_in_users = csv.DictReader(file)      
            for i in read_in_users:
                if user_name == (i['email']):
                    password = input('Enter your password: ') 
                    """ 
                    Not overly happy with this following part, but as i couldnt save a list into a csv file i had 
                    to use this piece of code to take string stored in csv and make it into a list,
                    next time i would use a database that i could store lists ie. sqllite, that seemed like a 
                    whole new kettle of fish and would have to restart a lot of code, so left it for now
                    
                    """
                    i = (i['password'].strip('[]').split(','))
                    password_list = []
                    for j in i:
                        password_list.append( int(j))
                    p = Encryption(password_list)
                    ## call OPT function if correct
                    if  password == p.decrypt():
                        enter_opt(user_name, first, last)
                        return
                    else: 
                        print("--------Incorrect Password---------")
                        if try_count == 2:                        
                            print('You have '+ str(try_count) +' attempts left')
                            try_count-=1
                        elif try_count == 1:
                            print('You have '+ str(try_count) +' attempt left')
                            try_count -=1
                        else: 
                            print('You are out of attempts')
                            first_screen()      

############## CHECKS A USER DOESNT ALREADY EXIST DURING SIGN UP STAGE AND FOR VALID EMAIL ##############
def check_user(user):
    ##### Check for valid email address,  Does user_name have an @ symbol
    if '@' not in user:
        print('Not a valid email address')
        return True
    else:
        ####### Checks given user name against database
        with open('user_log.csv', 'r') as file:
            reader = csv.DictReader(file)
            for usr in reader:
                if user == (usr['email']):
                    print('This email is already registered')
                    return True

############ TAKES USERS THROUGH FIRST SIGN UP ###############
def sign_up():
        print(':::::::::::: Please sign up :::::::::::')
        print('Use email address as user name')
        new_user_name = input('Enter a new user name: ')
        ### If user name not valid or already in database, suggest try different user name ###
        while check_user(new_user_name) == True:
            new_user_name = input('Try a different user name: ')        
        new_user_first = input('Enter you first name:')
        new_user_last = input('Enter your last name: ')
        new_password = input('Enter new password: ')
        # Encrypts  the password for storage in csv file
        encrypted_password = Encryption(new_password)
        #### With help from https://docs.python.org/3/library/csv.html
        with open('user_log.csv', 'a', newline='') as file:
            fieldnames = ['first_name', 'last_name', 'email', 'password', 'last_login']
            writer = csv.DictWriter(file, fieldnames= fieldnames)

            writer.writerow({'first_name':new_user_first,'last_name':new_user_last,'email':new_user_name,'password':encrypted_password.encrypt()})
        first_screen()

############## ASKS USER IF THEY ALREADY HAVE AN ACCOUNT #####################
def first_screen():
    log_or_sign = input('Do you already have an account? (y) or (n): ')
    if log_or_sign == 'y':
        login()
    elif log_or_sign == 'n':
        sign_up()
    else: 
        print('Not a valid response')
        exit() 

first_screen()
        
    








