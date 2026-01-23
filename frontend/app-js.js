function starting_after() {
    autosize(document.getElementById("send_message"));
    document.getElementById("add_new_chat").addEventListener("click", open_add_chat);
    document.getElementById("close_btn").addEventListener("click", close_add_chat);
    document.getElementById("add_btn").addEventListener("click", add_user_in_invitation);
    document.getElementById("send_invitation").addEventListener("click", create_new_chat);
}

async function get_data(user_id) {
    const data = await fetch((`http://localhost/api/data/user?id=${user_id}`), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    if (data.status === 200) {
        return data;
    } else if (data.status === 404) {
    }
}


async function load_chat(user_id, chat_id) {
    var data = await fetch((`http://localhost/api/data/messages?chat_id=${chat_id}&offset=0&limit=50`), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json',
            'Access-Token': localStorage.getItem("accessToken")
         }
    });
    data = await data.json();
    const chat_for_oponent = document.createElement("div");
    chat_for_oponent.id = "chat_for_oponent";

    for (message in data.messages) {
        const message_container = document.createElement("div") 
        if (message.sender == user_id) {
            message_container.classList.add("oponent message");
        } else {
            message_container.className = "user message";
        }
        message_container.textContent = data.messages[Number(message)].content;
        chat_for_oponent.append(message_container);
    }

    chat.innerHTML = '';
    chat.append(chat_for_oponent);
    
}

async function load_chat_container() {
    // Создание контейнера чата
    const chat_container = document.createElement("div");
    chat_container.id = "chat_container";


    const oponent_header = document.createElement("div");
    oponent_header.classList.add("oponent_header");

    const response_user_info = await get_data(this.id);

    if (response_user_info.status === 200) {
        let user_info = await response_user_info.json();
        user_info = user_info.users[0];
        const logo_oponent = document.createElement("img");
        logo_oponent.src = user_info.avatar_url;
        logo_oponent.alt = "logo_oponent";
        logo_oponent.className = "logo logo_oponent";
        logo_oponent.id = "logo_oponent";

        const oponent_info = document.createElement("div");
        oponent_info.classList.add("oponent_info")
        
        const oponent_name = document.createElement("p");
        oponent_name.classList.add("oponent_name");
        oponent_name.id = "oponent_name";
        oponent_name.textContent = user_info.nickname;

        const oponent_state = document.createElement("p");
        oponent_state.classList.add("state_oponent");
        oponent_state.textContent = ""; // TODO получать состояние опонента из запроса

        oponent_info.append(oponent_name, oponent_state);
        oponent_header.append(logo_oponent, oponent_info);


        const chat = document.createElement("div");
        chat.id = "chat";
        
        load_chat(this.id, document.getElementById(this.id).childNodes.item(0).id);

        const send = document.createElement("div");
        send.id = "send";

        const message_send = document.createElement("textarea");
        message_send.id = "send_message";
        message_send.placeholder = "Сообщение...";
        message_send.maxlength = "1000";
        message_send.rows = "1";

        const send_img = document.createElement("img");
        send_img.alt = "send";
        send_img.classList.add("used_logo");
        send_img.id = "message_send";

        send.append(message_send, send_img);


        chat_container.append(oponent_header, chat, send);

        const parent = document.getElementById("main_container");
        parent.append(chat_container);
        if (document.getElementById("wait_event")) {
            parent.removeChild(document.getElementById("wait_event"));
        } else {
            parent.removeChild(document.getElementById("chat_container"));
        }
        document.getElementById("message_send").addEventListener("click", send_message);
    }
}


function load_profile() {
    document.getElementById("logo_user").src = localStorage.getItem("avatar"); 
    document.getElementById("nickname").textContent = localStorage.getItem("nickname");
    document.getElementById("user_id").textContent = localStorage.getItem("id");
}


async function load_contacts() {
    const contacts = document.getElementById("contacts");
    
    contacts.innerHTML = "";

    const chats = JSON.parse(localStorage.getItem("chats"))

    for (let chat in chats) {
        const contact = document.createElement("div");
        contact.classList.add("contact");
        contact.id = chats[chat].ids[0];

        const view_contact = document.createElement("div");
        view_contact.classList.add("view_contact");
        view_contact.id = chat;

        const img = document.createElement("img");
        img.classList.add("logo");
        img.alt = "logo";
        img.src = await get_avatar_url_by_id(chats[chat].ids[0]);

        const name_contact = document.createElement("p");
        name_contact.classList.add("name_contact");
        name_contact.textContent = await get_nickname_by_id(chats[chat].ids[0]);

        view_contact.append(img, name_contact);

        const view_message = document.createElement("div");
        view_message.classList.add("view_message");
        view_message.textContent = chats[chat].last_message; // Добавить ссылку из бд

        contact.append(view_contact, view_message);
        contacts.append(contact);
    }

    clicked_contacts = document.getElementsByClassName("contact");

    for (let element = 0; element < clicked_contacts.length; element++) {
        clicked_contacts.item(element).addEventListener("click", load_chat_container, true);
    }
    // document.getElementById('chat_for_oponent').scrollIntoView;
}


async function get_avatar_url_by_id(id) {
    const response = await get_data(id);

    if (response.status == 200) {
        const data = await response.json();
        return data.users[0].avatar_url;
    }
}

async function get_nickname_by_id(id) {
    const response = await get_data(id);

    if (response.status == 200) {
        const data = await response.json();
        return data.users[0].nickname;
    }
}


async function create_chat(oponents_id) {
    console.log(oponents_id);
    await fetch(('http://localhost/api/data/chats'), {
        method: 'POST',
        headers: {  'Access-Token': localStorage.getItem("accessToken"),
                    'Content-Type': 'application/json' },
        body: JSON.stringify({
            "members_ids": oponents_id
        })
    });
    getProtectedData();
}


async function send_message() {
    var user_id = "", chat_id = "";
    for (let i = 0; i < document.getElementsByClassName("name_contact").length; i++) {
        if (document.getElementsByClassName("name_contact").item(i).textContent == document.getElementById("oponent_name").textContent){
            chat_id = document.getElementsByClassName("name_contact").item(i).parentNode.id;
            user_id = document.getElementsByClassName("name_contact").item(i).parentNode.parentNode.id;
            break;
        }
    }

    const input = document.getElementById("send_message");
    const message = input.value;
    input.value = "";
    
    await fetch(('http://localhost/api/data/messages'), {
        method: 'POST',
        headers: {  'Access-Token': localStorage.getItem("accessToken"),
                    'Content-Type': 'application/json' },
        body: JSON.stringify({
                "messages": [
                    {
                    "chat_id": chat_id,
                    "content": message,
                    "sender": user_id
                    }
                        ]
                })
    });

    await load_chat(user_id, chat_id);
}


function open_add_chat() {
    document.getElementById("overlay").style.visibility = "visible";
}

function close_add_chat() {
    let len = document.querySelectorAll(".added_user").length;
    for (let i = 0; i < len; i++) {
        document.getElementById("add_users").removeChild(document.querySelectorAll(".added_user").item(0));
    }
    document.getElementById("input_id").value = ""
    document.getElementById("overlay").style.visibility = "";
}

async function add_user_in_invitation() {
    var input_value = document.getElementById("input_id").value;
    if (input_value != "" && document.getElementById("add_users").childElementCount < 8) {
        for (let i = 0; i < document.getElementsByClassName("added_user").length; i++) {
            if (input_value == document.getElementsByClassName("added_user").item(i).getElementsByClassName("nickname_added_user").item(0).textContent){
                return
            }
        }
        for (let i = 0; i < document.getElementsByClassName("contact").length; i++){
            if (input_value == document.getElementsByClassName("contact").item(i).id) {
                return
            }
        }
        const response_user_info = await get_data(Number(input_value));

        if (response_user_info.status == 200) {
            const added_user = document.createElement("div");
            added_user.classList.add("added_user");

            const nickname_added_user = document.createElement("p")
            nickname_added_user.classList.add("nickname_added_user");
            nickname_added_user.textContent = input_value;
            nickname_added_user.value = input_value;

            const delete_user = document.createElement("img");
            delete_user.classList.add("used_logo", "delete_user");
            delete_user.alt = "delete";

            added_user.append(nickname_added_user, delete_user);
            document.getElementById("add_users").append(added_user);
        }
    }
}

function create_new_chat() {
    if (document.getElementsByClassName("added_user").length != 0){
        let list = [];
        for (let i = 0; i < document.getElementsByClassName("added_user").length; i++) {
                list.push(Number(document.getElementsByClassName("added_user").item(i).getElementsByClassName("nickname_added_user").item(0).textContent));
            }
        create_chat(list);
        close_add_chat();
    }
}