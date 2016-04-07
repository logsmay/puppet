import falcon

from routes import route_account, route_session

app = falcon.API()

##################
# Account routes #
##################
post_account = route_account.RoutePostAccount()
app.add_route('/post_account', post_account)

##################
# Session routes #
##################
post_session = route_session.RoutePostSession()
app.add_route('/post_session', post_session)

delete_session = route_session.RouteDeleteSession()
app.add_route('/delete_session', delete_session)