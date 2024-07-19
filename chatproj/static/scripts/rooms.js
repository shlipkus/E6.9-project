let list_room = document.querySelector('#list-room');
let create_room = document.querySelector('#create');
let crtBtn = document.querySelector('#btn_add');

function addElem(resp) {
    for(let value of resp.results) {
        let el = document.createElement("p");
        let btn = document.createElement("button");
        btn.innerHTML = 'Присоединиться';
        btn.id = value.slug;
        btn.addEventListener('click', () => {
            window.location.href = `/rooms/${value.slug}`;
        })
        el.innerHTML = `${value.chat_name} (${value.description}). Хост: ${value.host_name} `;
        el.appendChild(btn);
        list_room.appendChild(el);
        console.log(value);
    }
}

function createAddForm() {
    create_room.replaceChildren();
    let pl = document.createElement("p");
    let pt = document.createElement("p");
    let btnSub = document.createElement("button");
    let btnDis = document.createElement("button");
    btnSub.innerHTML = 'Создать';
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
        crtBtn.disabled = false;
        create_room.replaceChildren();;
    })

    btnSub.addEventListener('click', () => {
        crtBtn.disabled = false;
        create_room.replaceChildren();
        postData("http://127.0.0.1:8000/api/public_chats/", { chat_name: inpName.value, description: inpDes.value }).then((data) => {
                                  window.location.href = `/rooms/${data.slug}`; // JSON data parsed by `response.json()` call
                                });
    })
}


crtBtn.addEventListener('click', () => {
    crtBtn.disabled = true;
    createAddForm();
})

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

async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
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

fetch('http://127.0.0.1:8000/api/public_chats/')
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    addElem(data);
  });


