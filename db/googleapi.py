import os
from binascii import hexlify
from google.cloud import datastore
import hashlib
import base64
# Create, populate and persist an entity with keyID=1234

# Instantiates a client
#CAn create an abstraced parent class that handles entity kind and such
class User:
    '''USer control, accepts email as 'key', if the email exists should contain
    the user object'''
    kind = 'User'
    def __init__(self, email):
        self.email = email
        self.client = datastore.Client()
        self.entity = datastore.Entity(self.client.key('User'))
        self.get_user()

    def get_user(self):
        '''Try to get user object from db'''
        self.query = self.client.query(kind=self.kind)
        self.query = self.query.add_filter('email', '=', self.email)
        self.obj = self.query.fetch(1)
        try: self.obj= list(self.obj)[0]
        except: pass

        if self.exists():
            print(self.exists())
            self.user = self.obj #user is just the first thing returned
            self.id = self.user.id
            self.key = self.client.key(self.kind, self.id)

    def exists(self):
        '''Returns True or False on if the email exists'''
        if isinstance(self.obj,datastore.Entity):
            return True
        else:
            return False
    
    def create(self, first, last, password):
        '''Creates account only if the email isn't used'''
        if self.exists():
            raise ValueError('Email already exists.')

        else:
            self.add('email',self.email)
            self.add('first_name', first)
            self.add('last_name', last)
            self.add('password',  self.hashed(password))
            self.add('verified_email',  False)
            self.add('account_type',  'standard')
            self.client.put(self.entity)
            self.get_user() # load user after creating for futher manipulations
            
    def delete(self):
        '''Deletes account '''
        
        if self.exists():
            batch = self.client.batch()
            with batch:
                batch.delete(self.key)
        else:
            raise ValueError('Can\'t delete non-existant account.')
    
    def add(self, key, value):
        '''Just adds field to entity object from get_user func'''
        self.entity[key] = value

    def new_api_key(self):
        '''Generates api key'''
        return hexlify(os.urandom(32))
    
    def new_pass(self):
        '''Create new password'''
        pass
    
    def hash(self, password, salt= None):
        m = hashlib.sha256()
        m.update(bytes(password,'utf-8'))

        if salt == None:
            self.make_salt()
            print(f'Creation salt: {self.salt}')
            m.update(self.salt)
        else:
            m.update(salt)
        hashed = base64.b64encode(m.digest()) 

        return hashed

    def hashed(self, password):
        '''returns sha256+salted output with salt as sha256output:salt'''
        #print(f'Storage salt: {self.salt}')
        return self.hash(password).decode('utf-8') + ':' + str(int.from_bytes(self.salt,byteorder='big'))

    def make_salt(self):
        '''Generates password salte'''
        self.salt = os.urandom(32)
        return self.salt

    def get_password(self):
        self.passw = self.obj.get('password')
    
    def split_salt(self): 
        self.get_password()      
        return self.passw.split(':')
    
    def verify_password(self, password):
        sha, salt = self.split_salt()
        salt = bytes(salt,'utf-8')
        
        hashed = self.hash(password, salt = salt)
        #print(hashed.decode('utf-8'))
        sha = sha
        print(sha, hashed, salt)

user = User('Michael-fore@sbcglobal.net')
#user.create('Michael','Fore','Hello_World')
#user.delete()
print(user.exists())
user.verify_password('Hello_World')
