import flask_login
import os
from binascii import hexlify
from google.cloud import datastore
import hashlib
import base64

#
# flask login handles the session cookies
#
login_manager = flask_login.LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


# Create, populate and persist an entity with keyID=1234

# Instantiates a client
#CAn create an abstraced parent class that handles entity kind and such
class Hasher:
    
    def hash(self, password, salt= None):
        m = hashlib.sha256()
        m.update(bytes(password,'utf-8'))

        if salt == None:
            self.make_salt()
            print(f'Creation salt: {self.salt}')
            print(f"Creation salt int: {int.from_bytes(self.salt,byteorder='big')}")
            m.update(self.salt)
        else:
            m.update(salt)
        hashed = base64.b64encode(m.digest()) 

        return hashed

    def hashed(self, password):
        '''returns sha256+salted output with salt as sha256output:salt'''
        #self.make_salt()
        
        return self.hash(password).decode('utf-8') + ':' + str(int.from_bytes(self.salt,byteorder='big'))

    def make_salt(self):
        '''Generates password salte'''
        self.salt = os.urandom(32)
        return self.salt

class Control:
    '''future holder of crud for the user object'''
    pass

class User(Hasher):
    '''USer control, accepts email as 'key', if the email exists should contain
    the user object'''
    kind = 'User'
    def __init__(self):
        self.client = datastore.Client()
        self.entity = datastore.Entity(self.client.key('User'))
        

    def get_id(self, email):
        '''Try to get user object from db'''
        self.email = email
        self.query = self.client.query(kind=self.kind)
        self.query = self.query.add_filter('email', '=', self.email)
        self.obj = self.query.fetch(1)
        try: self.obj= list(self.obj)[0]
        except: pass

        if self.exists():
            self.user = self.obj #user is just the first thing returned
            self.id = self.user.id
            self.key = self.client.key(self.kind, self.id)
            self.is_authenticated = self.user.get('verified')
            self.is_active = self.user.get('active')
            self.is_anonymous = self.user.get('is_anonymous')
        else:
            return None

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
            self.add('verified', True)
            self.add('active', True)
            self.add('is_anonymous',  False)
            self.add('account_type',  'standard')
            self.client.put(self.entity)
            self.get_id(self.email) # load user after creating for futher manipulations
            
    def delete(self):
        '''Deletes account '''
        
        if self.exists():
            batch = self.client.batch()
            with batch:
                batch.delete(self.key)
        else:
            raise ValueError('Can\'t delete non-existant account.')
    
    def add(self, key, value):
        '''Just adds field to entity object from get_user func. doesn't push to db'''
        self.entity[key] = value

    def update(self, key, value):
        '''Updates a field the pushes it to the db'''
        self.user[key] = value
        print(f'updated :{key, value}')
        self.client.put(self.user)

    def new_api_key(self):
        '''Generates api key'''
        return hexlify(os.urandom(32))
    
    def new_pass(self, password):
        '''Create new password'''
        self.update('password', self.hashed(password))

    def get_password(self):
        '''Retrieves password from db'''
        self.passw = self.obj.get('password')
    
    def split_salt(self): 
        '''Password is stored in db and sha:salt'''
        self.get_password()      
        return self.passw.split(':')
    
    def verify_password(self, password):
        ''' return true if the user password input + stored salt sha matches the
        sha created on account creation'''
        sha, salt = self.split_salt()
        salt = int(salt).to_bytes(32, byteorder="big") #32 is the size for os.urand
        hashed = self.hash(password, salt = salt)
       
        if hashed == bytes(sha, 'utf-8'):
            return True
        else:
            return False
        
    

user = User()
user.get_id('Michael-fore@sbcglobal.net')
#user.create('Michael','Fore','Hello_World')
#user.delete()

x = user.verify_password('Cat')
#user.new_pass('Cat')
print(x)
