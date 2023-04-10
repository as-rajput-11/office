import asyncio, websockets, soundfile, io
import speech_recognition as sr
r=sr.Recognizer()
async def hello(websocket):
    while True:
        try:
            req = await websocket.recv()
            data, samplerate = soundfile.read(io.BytesIO(req))
            soundfile.write('a.wav', data, samplerate, subtype='PCM_32')
            with sr.AudioFile('a.wav')as source:
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    await websocket.send(text)
                    print(text)
                except:
                    pass
        except websockets.ConnectionClosed:
            break
async def main():
    async with websockets.serve(hello, 'localhost', 8865):
        await asyncio.Future()
if __name__ == '__main__':
    asyncio.run(main())