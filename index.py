import falcon

from routes import route_account

app = falcon.API()

post_account = route_account.RoutePostAccount()

app.add_route('/post_account', post_account)
