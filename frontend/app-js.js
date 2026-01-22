function starting_after() {
    autosize(document.getElementById("send_message"));
    document.querySelectorAll(".contact").forEach(item => {item.addEventListener("click", load_chat_container(item.id))});
    document.getElementById("add_new_chat").addEventListener("click", open_add_chat);
    document.getElementById("close_btn").addEventListener("click", close_add_chat);
    document.getElementById("add_btn").addEventListener("click", add_user_in_invitation);
    document.getElementById("send_invitation").addEventListener("click", create_new_chat);
}


function load_chat_container(oponent_id) {
    // Создание контейнера чата
    const chat_container = document.createElement("div");
    chat_container.id = "chat_container";


    const oponent_header = document.createElement("div");
    oponent_header.classList.add("oponent_header");

    const response_user_info = fetch((`http://localhost/api/data/user?id=${oponent_id}`), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    const user_info = response_user_info.json()[0];
    
    const logo_oponent = document.createElement("img");
    logo_oponent.src = user_info.avatar_url;
    logo_oponent.alt = "logo_oponent";
    logo_oponent.classList.add(["logo", "logo_oponent"]);
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
    
    const chat_for_oponent = document.createElement("div");
    chat_for_oponent.id = "chat_for_oponent";

    // Получение истории и создание чата
    const response = fetch((`http://localhost/api/data/messages?chat_id=${oponent_id}&offset=0&limit=50`), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    const data = response.json();
    for (message in data) {
        const message_container = document.createElement("div") 
        if (message.sender == oponent_id) {
            message_container.classList.add("oponent_message");
        } else {
            message_container.classList.add("user_message");
        }
        message_container.textContent = message.content;
        chat_for_oponent.append(message_container)
    }

    chat.append(chat_for_oponent);


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
    parent.insertBefore(chat_container, document.getElementById("view_container"));
    parent.remove(document.getElementById("wait_event"));
}


function load_profile() {
    document.getElementById("logo_user").src = localStorage.getItem("avatar"); 
    document.getElementById("nickname").textContent = localStorage.getItem("nickname");
    document.getElementById("user_id").textContent = localStorage.getItem("id");
}


async function load_contacts() {
    const contacts = document.getElementById("contacts");
    const chats = JSON.parse(localStorage.getItem("chats"));

    for (let chat in chats) {
        const contact = document.createElement("div");
        contact.classList.add("contact");

        const view_contact = document.createElement("div");
        view_contact.classList.add("view_contact");

        const img = document.createElement("img");
        img.classList.add("logo");
        img.alt = "logo";
        img.src = await get_avatar_url_by_id(chats[chat].ids[0]);

        const name_contact = document.createElement("p");
        name_contact.classList.add("name_contact");
        name_contact.textContent = chats[chat];

        view_contact.append(img, name_contact);

        const view_message = document.createElement("div");
        view_message.classList.add("view_message");
        view_message.textContent = chats[chat][nickname]; // Добавить ссылку из бд

        contact.append(view_contact, view_message);
        contacts.append(contact);
    }

    // document.getElementById('chat_for_oponent').scrollIntoView;
}


async function get_avatar_url_by_id(id) {
    const response = await fetch(
        `http://localhost/api/data/user?id=${id}`,
        {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            },
        }
    );

    if (response.status == 200) {
        const data = await response.json();
        return data[0].avatar_url;
    }
}


async function create_chat(oponents_id) {
    console.log(oponents_id);
    await fetch(('http://localhost/api/data/chats'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "members": oponents_id
        })
    });
    await load_contacts();
}


async function send_message(chat_id) {
    const input = document.getElementById("send_message");
    const message = input.textContent;
    const user_id = localStorage.getItem("id");
    input.textContent = "";
    
    await fetch(('http://localhost/api/data/messages'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: {
            "chat_id": chat_id,
            "content": message,
            "sender": user_id
        }
    });
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

function add_user_in_invitation() {
    if (document.getElementById("input_id").value != "" && document.getElementById("add_users").childElementCount < 8) {
        for (let i = 0; i < document.getElementsByClassName("added_user").length; i++) {
            if (document.getElementById("input_id").value == document.getElementsByClassName("added_user").item(i).getElementsByClassName("nickname_added_user").item(0).textContent){
                return
            }
        }
        const added_user = document.createElement("div");
        added_user.classList.add("added_user");

        const nickname_added_user = document.createElement("p")
        nickname_added_user.classList.add("nickname_added_user");
        nickname_added_user.textContent = document.getElementById("input_id").value;
        nickname_added_user.value = document.getElementById("input_id").value;

        const delete_user = document.createElement("img");
        delete_user.classList.add("used_logo", "delete_user");
        delete_user.alt = "delete";

        added_user.append(nickname_added_user, delete_user);
        document.getElementById("add_users").append(added_user);
        
    }
}

function create_new_chat() {
    let list = [];
    for (let i = 0; i < document.getElementsByClassName("added_user").length; i++) {
            list.push(Number(document.getElementsByClassName("added_user").item(i).getElementsByClassName("nickname_added_user").item(0).textContent));
        }
    create_chat(list);
    close_add_chat();
}