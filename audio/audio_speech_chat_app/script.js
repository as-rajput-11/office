// Websocket

const webSocket = new WebSocket('ws://localhost:8888/websocket');

webSocket.onopen = function () {
    console.log('WebSocket connection established');
    const name = prompt('What is your name: ')
    webSocket.send(name);
};

webSocket.onmessage = function (event) {
    const message = event.data;
    messageDict = processMessage(message)
    const nameColor = processColour(messageDict['user_colour'])

    // name element
    const nameElem = document.createElement('span')
    nameElem.classList.add('fw-bold')
    nameElem.style.color = nameColor
    nameElem.innerHTML = messageDict['name']
    messagesOutput.appendChild(nameElem)

    // add message
    messagesOutput.innerHTML += `: ${messageDict['message']}`

    // add linebreak
    let lineBreak = document.createElement('br')
    messagesOutput.appendChild(lineBreak)
};

webSocket.onclose = function (event) {
    console.log('WebSocket connection closed with code ' + event.code);
    let closeElem = document.createElement('span')
    closeElem.classList.add('text-secondary')
    closeElem.innerHTML = 'Websocket connection closed';
    messagesOutput.appendChild(closeElem)
};

// Events

const messageInput = document.getElementById('message-input');
const messagesOutput = document.getElementById('messages');
const sendButton = document.getElementById('send-button');
const closeButton = document.getElementById('close-button');
const s_text = document.getElementById('s_text');

messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault()
        sendMessage();
    }
});


// s_text.addEventListener('click', function () {
//     sendMessage();
// });

sendButton.addEventListener('click', function () {
    sendMessage();
});

closeButton.addEventListener('click', function () {
    webSocket.close();
});

messagesOutput.addEventListener('DOMSubtreeModified', scrollToBottom);

// Functions

function sendMessage() {
    const message = messageInput.value;
    if (message) {
        webSocket.send(message);
    }
    messageInput.value = '';
}

function scrollToBottom() {
    messagesOutput.scrollTop = messagesOutput.scrollHeight;
}

function processMessage(message) {
    return JSON.parse(message)
}

function processColour(colour) {
    return `rgb(${colour[0]}, ${colour[1]}, ${colour[2]})`
}

var mr, ws
function send() {
    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(s => {
        mr = new MediaRecorder(s);
        audioChunks = []
        mr.ondataavailable = e => {
            audioChunks.push(e.data);
            let blob = new Blob(audioChunks, {
                type: 'audio/x-mpeg-3'
            });
            ws.send(blob)
        }
        ws = new WebSocket('ws://localhost:8888/websocket')

        ws.onmessage = d => {
            if(!d.data.includes('{'))
            document.getElementById('message-input').value = d.data + " "
        //     ws.close()
        }
        mr.start()
    })
}
function stop() {
    mr && mr.state == 'recording' && mr.stop()
}
// function clr() {
//     document.getElementById('message-input').innerText = ''
// }