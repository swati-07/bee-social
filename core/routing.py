from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import Social.routing
application= ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter(
			Social.routing.websocket_urlpatterns
			)
		),
	})