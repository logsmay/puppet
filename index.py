import falcon

from routes import route_account, route_session, route_shipper

app = falcon.API()

# ## Routes ## #

account = route_account.RouteAccount()
app.add_route('/account', account)

session = route_session.RouteSession()
app.add_route('/session', session)

shipper = route_shipper.RouteShipper()
app.add_route('/session', shipper)
