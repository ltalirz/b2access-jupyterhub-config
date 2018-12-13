c = get_config()

# ... here goes your specific JupyterHub setup

#===============================================================================
# use OAuth2 via B2ACCESS
from oauthenticator.generic import GenericOAuthenticator, GenericEnvMixin

auth_server = "https://unity.eudat-aai.fz-juelich.de"  # start by registering with b2access test server
#auth_server = "https://b2access.eudat.eu"

c.JupyterHub.authenticator_class = GenericOAuthenticator
GenericEnvMixin._OAUTH_AUTHORIZE_URL = auth_server + "/oauth2-as/oauth2-authz"

GenericOAuthenticator.login_service = "B2ACCESS"
GenericOAuthenticator.enable_auth_state = True

c.GenericOAuthenticator.client_id = "aiidalab-demo"   # user name of b2access registration
c.GenericOAuthenticator.oauth_callback_url = "https://aiidalab-demo.materialscloud.org/hub/oauth_callback" # oauth callback url
c.GenericOAuthenticator.token_url = auth_server + "/oauth2/token"
c.GenericOAuthenticator.client_secret = "afakepw"  # password credential in b2access registration
c.GenericOAuthenticator.userdata_url = auth_server + "/oauth2/userinfo"

# Requesting the profile and email scopes will return a json of the form:
# {'sub': '12344556-ewrf-4105-23sgerrs4t3esefde', 'email': 'leopold.talirz@gmail.com', 'name': 'Leopold Talirz'}
c.GenericOAuthenticator.scope = ['profile', 'email']

# This uses the email address as the JupyterHub user name.
# (Alternative: use the unique 'sub' identifier of B2ACCESS)
c.GenericOAuthenticator.username_key = 'email'

#===============================================================================
# overwrite logout handler to also log out of B2ACCESS
# https://github.com/jupyterhub/jupyterhub/blob/master/jupyterhub/handlers/login.py#L14
import urllib.parse
import requests

#from tornado import gen
#@gen.coroutine()
async def logout_handler(self):
    self.clear_login_cookie()
    self.statsd.incr('logout')
    next = urllib.parse.quote("/hub/login")

    user = self.get_current_user()
    if not user:
        self.log.error("Unable to get_current_user for logout")
        return self.redirect(next, permanent=False)

    self.log.info("User logged out: %s", user.name)

    auth_state = await user.get_auth_state()
    if auth_state is None:
        self.log.warn("Unable to revoke OAuth token for user '%s': auth_state missing", user.name)
        return self.redirect(next, permanent=False)

    # TODO: Make this async / switch to coroutine
    r = requests.post(auth_server + "/oauth2/revoke",
        headers={ 'Content-Type': 'application/x-www-form-urlencoded'},
        data={ 'token': auth_state['access_token'],
               'client_id': c.GenericOAuthenticator.client_id,
               'token_type': 'Bearer',
               'token_type_hint': 'access_token',
        }
    )
    r.raise_for_status()
    self.log.warn("Revoked OAuth token for user '%s'", user.name)

    return self.redirect(next, permanent=False)
    

from jupyterhub.handlers.login import LogoutHandler
LogoutHandler.get = logout_handler
