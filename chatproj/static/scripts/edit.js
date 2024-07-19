const id = JSON.parse(document.getElementById('id-pk').textContent);
const chatName = JSON.parse(document.getElementById('name').textContent);
const chatDesc = JSON.parse(document.getElementById('desc').textContent);
let create_room = document.querySelector('#create');
let edBtn = document.querySelector('#btn_edit');
let delBtn = document.querySelector('#btn_delete');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function createAddForm() {
    create_room.replaceChildren();
    let pl = document.createElement("p");
    let pt = document.createElement("p");
    let btnSub = document.createElement("button");
    let btnDis = document.createElement("button");
    btnSub.innerHTML = 'Сохранить';
    btnDis.innerHTML = 'Отмена';
    let inpName = document.createElement("input");
    let inpDes = document.createElement("textarea");
    inpDes.rows = '10';
    inpDes.cols = '60';
    pl.innerHTML = 'Название: <br>';
    pt.innerHTML = 'Описание: <br>';
    pl.appendChild(inpName)
    create_room.appendChild(pl);
    pt.appendChild(inpDes)
    create_room.appendChild(pt);
    create_room.appendChild(btnSub);
    create_room.appendChild(btnDis);
    btnDis.addEventListener('click', () => {
        edBtn.disabled = false;
        create_room.replaceChildren();;
    })

    btnSub.addEventListener('click', () => {
        result = confirm('Вы уверены?');
        if(result){
            let nameChat = inpName.value
            let desc = inpDes.value
            if(inpName.value == ""){
                nameChat = chatName;
            }
            if(inpDes.value == ""){
                desc = chatDesc;
            }
            edBtn.disabled = false;
            create_room.replaceChildren();
            putData('http://127.0.0.1:8000/api/public_chats/'+id+'/',
            { chat_name: nameChat, description: desc }).then((data) => {
                                      window.location.href = `/rooms/${data.slug}`;
                                    });
        }
    })

}

edBtn.addEventListener('click', () => {
    edBtn.disabled = true;
    createAddForm();
})

delBtn.addEventListener('click', () => {
    result = confirm('Вы уверены что хотите удалить чат?');
    if(result){
    deleteData('http://127.0.0.1:8000/api/public_chats/' + id + '/')
    .then((data) => {
        window.location.href = '/rooms/';
    })
    }
})


async function putData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "PUT", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken,
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *client
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return await response.json(); // parses JSON response into native JavaScript objects
}

async function deleteData(url = "") {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "DELETE", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken,
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *client
  });
  return
}
