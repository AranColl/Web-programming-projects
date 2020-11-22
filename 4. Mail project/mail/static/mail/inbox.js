document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', function(){compose_email(null)});

  // By default, load the inbox
  load_mailbox('inbox');
});

function submit_form() {

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        if(result.error){
            alert(error);
            console.log(error);
            alert('inside submit');
        }

    });

    return false;
}

function compose_email(reply_email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (reply_email === null){
      // Clear out composition fields
      document.querySelector('#compose-recipients').value = '';
      document.querySelector('#compose-subject').value = '';
      document.querySelector('#compose-body').value = '';

  }else{
      // Clear out composition fields
      document.querySelector('#compose-recipients').value = reply_email.sender;
      document.querySelector('#compose-subject').value = 'Re:' + reply_email.subject;
      document.querySelector('#compose-body').value = 'On ' + reply_email.timestamp + ' ' + reply_email.sender + ' wrote: ' + reply_email.body;
  }


  //listen to the compose email form
  document.querySelector('#compose-form').addEventListener('submit', submit_form);


}

function get_email(id){
    var node= document.getElementById("emails-view");
    node.querySelectorAll('*').forEach(n => n.remove());


    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        archive_read(email, 'read', true);

        const element = document.createElement('div');
        element.className = 'email';
        document.getElementById('emails-view').append(element)

        const par = document.createElement('p');
        par.innerHTML = `<b>From: </b> ${email.sender} <br>
        <b>To: </b> ${email.recipients} <br>
        <b>Subject: </b> ${email.subject} <br>
        <b>Timestamp: </b> ${email.timestamp} <br><hr>
        ${email.body} <hr>`;
        document.querySelector('.email').append(par);

        const reply_button = document.createElement('button');
        reply_button.className = 'delete_button';
        reply_button.innerHTML = 'Reply';
        reply_button.addEventListener('click',function(){compose_email(email)});
        document.querySelector('.email').append(reply_button);

        if(email.archived){
            const archive_button = document.createElement('button');
            archive_button.innerHTML = 'Unarchive';

            archive_button.addEventListener('click',function(){archive_read(email, 'archive', false)});
            document.querySelector('.email').append(archive_button);
        }else{
            const archive_button = document.createElement('button');
            archive_button.innerHTML = 'Archive';

            archive_button.addEventListener('click',function(){archive_read(email, 'archive', true)});
            document.querySelector('.email').append(archive_button);
        }


    });

    return false;
}

async function archive_read(email, action, bool){
        try{

            if (action == 'archive'){
                await fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      archived: bool
                  })
                })
                load_mailbox('inbox');
            }else{
                await fetch(`/emails/${email.id}`, {
                  method: 'PUT',
                  body: JSON.stringify({
                      read: true
                  })
                })
            }



    } catch (error) {
        alert(error);
    }
}

async function show_emails(mailbox){
  try {
    const response = await fetch(`/emails/${mailbox}`);
    const parsedResponse = await response.json();
    console.log(parsedResponse);

    parsedResponse.forEach(email => {
      const element = document.createElement('div');
      element.className = 'email_box';

      //define background depending whether the mail has been read
      if(email.read){ element.setAttribute("style", "background-color: #BDBDBD;");
      }else{ element.setAttribute("style", "background-color:#FFFFFF;"); }

      document.getElementById('emails-view').append(element);


      const para = document.createElement('p');
      para.innerHTML = `<b>From: </b> ${email.sender} <br>  <b>Subject: </b> ${email.subject} <br> ${email.timestamp}`;
      para.addEventListener('click', function(){get_email(email.id)});

      var elements = document.getElementsByClassName('email_box');
      var last_element = elements[elements.length - 1]
      last_element.append(para);

    });
  } catch (error) {
    //alert(error);
    console.log(error);
    //alert('inside show mails');
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //call a function to show the emails
  show_emails(mailbox);
}