document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Set links up to load new pages.
    document.querySelectorAll('.but').forEach(link => {
        link.onclick = () => {
            const page = link.dataset.page;
            window.location.href = document.URL + 'chat/' + page;
            return false;
        };
    });
  //Announce a new chatroom with sockets
  socket.on('connect', () => {
    document.querySelector('#hidenform').onsubmit = () => {
            const message = document.querySelector('#task').value;
            socket.emit('create chatroom', {'selection': message});
            document.querySelector('#task').value = '';
            return false;
        };
    });
    //Create the new chatroom if it does not exist yet
    socket.on('announce chatroom', data => {
        if(data.selection == "exists") {
            alert('Existing chatroom name!');
        }
        else {
            window.location.href = document.URL + 'chat/' + data.selection;

        }
    });
  //Display form to create new chatrooms only when requested. By default, hidden.
  document.querySelector('#hidenform').style.display = "none";

  document.querySelector('#hide').onclick = () =>{
    if(document.querySelector('#hidenform').style.display === "none"){
      document.querySelector('#hidenform').style.display = "block";
    }else{
      document.querySelector('#hidenform').style.display = "none";
    }
  };

  // By default, submit button is disabled
  document.querySelector('#submit').disabled = true;

  // Enable button only if there is text in the input field
  document.querySelector('#task').onkeyup = () => {
      if (document.querySelector('#task').value.length > 0)
          document.querySelector('#submit').disabled = false;
      else
          document.querySelector('#submit').disabled = true;
  };
});
