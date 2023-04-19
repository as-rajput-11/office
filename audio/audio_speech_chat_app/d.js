       ws.onmessage = d => {
            console.log(d)
            var url = URL.createObjectURL(d.data);
            var preview = document.createElement('audio');
            preview.controls = true;
            preview.src = url;
            document.body.appendChild(preview);
            // if(!d.data.includes('{'))
            console.log(d)
            document.getElementById('message-input').value = preview

            // document.getElementById('message-input').value = d.data + " "
        //     ws.close()
        }
        mr.start()
    })
