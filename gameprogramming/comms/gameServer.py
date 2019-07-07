import eventlet
import socketio
import eventlet.wsgi

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    
@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.on("update")
def update(sid, data):
    print(data)
    sio.emit('message', {'sender': sid , 'echo': data}, broadcast=True)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
