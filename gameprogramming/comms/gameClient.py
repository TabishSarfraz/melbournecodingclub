import socketio

sio = socketio.Client()
tank = {'id':'', 'team':'', 'x':-1, 'y':-1, 'bulletX':-1, 'bulletY':-1}
@sio.event
def connect():
    print('connection established')

@sio.on('message')
def my_message(data):
    if(data['sender']!=sio.sid):
        print('\n',data['sender']+": ", data['echo'])
        tank['id'] = data['echo']['id']
        tank['team'] = data['echo']['team']
        tank['x'] = data['echo']['x']
        tank['y'] = data['echo']['y']
        tank['bulletX'] = data['echo']['bulletX']
        tank['bulletY'] = data['echo']['bulletY']
#sio.emit('my response', {'response': 'my response'})

def getTank():
    return tank

@sio.event
def disconnect():
    print('disconnected from server')


def getID():
    return sio.sid

def send(mes):
    sio.emit('update', mes)

def makeConnection():
    sio.connect('http://localhost:5000')


def run():
    makeConnection()
    i = ""

    while i is not "q":
        mes = input("You:")
        sio.emit('update', mes)
    sio.wait()

if __name__=="__main__":
    run()
