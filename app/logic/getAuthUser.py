from app.allImports import *
from app.logic.redirectBack import redirect_url
import os


class AuthorizedUser:

    '''
    initializes the authorized user class
    @param username - name of the user accessing the information
    @param prefix   - prefix of the subject being accessed
    '''

    def __init__(self, prefix = None):
        # @private
        self.username = authUser(request.environ)
        self.prefix = prefix

    '''
    returns the username of the user
    '''
    def getUsername(self):
        return self.username
        
        
    '''
    checks to see if the user is an admin
    @public
    '''

    def isAdmin(self):
        user = User.select().where(User.username == self.username)
        if user.exists():
            user = user.get()
            return user.isAdmin
        else:
            return None
        

    '''
    check to see if the user is a division chair
    @private
    '''

    def isDivisionChair(self):
        subject = self.getSubject()

        return DivisionChair.select().where(
            DivisionChair.username == self.username).where(
            DivisionChair.did == subject.pid.division.dID).exists()

    '''
    check to see if the user is program chair
    @private
    '''

    def isProgramChair(self):
        subject = self.getSubject()

        return ProgramChair.select().where(
            ProgramChair.username == self.username).where(
            ProgramChair.pid == subject.pid.pID).exists()
    '''
    gets the subject we are trying to get
    @private
    '''

    def getSubject(self):
        return Subject.get(Subject.prefix == self.prefix)

    '''
    checks to see if user is program chair, admin, or division chair
    @public
    '''

    def isAuthorized(self):
        isAdminBool = self.isAdmin()
        isProgramChairBool = self.isProgramChair()
        isDivisionChairBool = self.isDivisionChair()
        return(isAdminBool or isProgramChairBool or isDivisionChairBool)
        
    def not_user(self):
        #Grab their user level
        description = request.environ['description']
        if description != 'student':
            try:
                addUser = User(username   = self.username,
                               firstname  = request.environ['givenName'],
                               lastname   = request.environ['sn'],
                               email      = request.environ['mail'],
                               isAdmin    = 0,
                               lastVisted = None)
                addUser.save(force_insert = True)
                #TODO: Add a redirect
            except:
                message = "Could not make account for username: {}".format(self.username)
                #TODO: Log here
                # redirect to 404
        else: 
            # redirect to 404
            return None
