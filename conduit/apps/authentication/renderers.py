from conduit.apps.core.renderers import ConduitJSONRenderer
class UserJSONRenderer(ConduitJSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer,self).render(data)