import smtplib
import csv
import random

class Otp:
    def __init__(self, user_info, one_time):
        self.user_info = user_info
        self.one_time = str(one_time)

#### With assistance from https://automatetheboringstuff.com/chapter16/
    def send_mail(self):
        print(self.one_time)
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo()
        s.login('2fa.authenticator@gmail.com','Passwrd1987')
        s.sendmail('2fa.authenticator@gmail.com', (self.user_info) , 'Subject: App 2fa Code\n' +(self.one_time))
        s.close() 

###### GENERATES A ONE TIME PASSWORD ######
def generate_otp():
    random_num = random.randint(100000,999999)
    return random_num

def enter_opt(users):
    send_otp = generate_otp()
    v = Otp(users, send_otp)
    v.send_mail()
    enter = int(input("Enter your one time password: "))
    if send_otp == enter:
        print('Welcome ')
    else: print('try again')

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
    with open('user_log.csv', 'r') as file:
        print('*********Welcome, Please Sign In********')
        user_name = input('Enter your user name: ')
        password = input('Enter your password: ')
        read_in_users = csv.DictReader(file)
        for i in read_in_users:
            if user_name == (i['email']):
                name = (i['first_name'])
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
                if  password == p.decrypt():
                    enter_opt(user_name)
                    
                else: print('password failed')
                

############## CHECKS A USER DOESNT ALREADY EXIST DURING SIGN UP STAGE ##############
def check_user(user):
    with open('user_log.csv', 'r') as file:
        reader = csv.DictReader(file)
        for usr in reader:
            if user == (usr['email']):
                print('This email is already registered')
                return True

############ TAKES USERS THROUGH FIRST SIGN UP ###############
def sign_up():
        print('Use email address as user name')
        new_user_name = input('Enter a new user name: ')
        ### If password already in database suggest try different user name ###
        while check_user(new_user_name) == True:
            new_user_name = input('Try a different user name: ')
        
        new_user_first = input('Enter you first name:')
        new_user_last = input('Enter your last name: ')
        new_password = input('Enter new password: ')
        # This line encrypts  the password for storage in csv file
        encrypted_password = Encryption(new_password)
        #### With help from https://docs.python.org/3/library/csv.html
        with open('user_log.csv', 'a', newline='') as file:
            fieldnames = ['first_name', 'last_name', 'email', 'password']
            writer = csv.DictWriter(file, fieldnames= fieldnames)

            writer.writerow({'first_name':new_user_first,'last_name':new_user_last,'email':new_user_name,'password':encrypted_password.encrypt()})

############## ASKS USER IF THEY ALREADY HAVE AN ACCOUNT #####################
def first_screen():
    log_or_sign = input('Do you already have an account? (y) or (n): ')
    if log_or_sign == 'y':
        login()
    elif log_or_sign == 'n':
        sign_up()
    else: exit() 

first_screen()
        
    








