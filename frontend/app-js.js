function load_chat_container(oponent_id) {
    const response_user_info = fetch(('http://127.0.0.1/data/user/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({"users_ids":[oponent_id]})
    });
    user_info = response_user_info.json();
    document.getElementById("logo_oponent").src = user_info.avatar_url;
    document.getElementById("oponent_name").textContent = user_info.nickname;

    const response = fetch(('http://127.0.0.1/data/messages/' + oponent_id), {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    data = response.json();
    chat = document.getElementById("chat_for_oponent")
    for (message in data) {
        message_container = document.createElement("div") 
        if (message.sender == oponent_id) {
            message_container.class = "oponent message";
        } else {
            message_container.class = "user message";
        }
        message_container.textContent = message.content;
        chat.append(message_container)
    }
}

function load_profile() {
    document.getElementById("logo_user").src = localStorage.getItem("avatar"); 
    document.getElementById("nickname").textContent = localStorage.getItem("nickname");
    document.getElementById("user_id").textContent = localStorage.getItem("id");
}
async function load_contacts() {
    contacts = document.getElementById("contacts");
    chats = JSON.parse(localStorage.getItem("chats"));

    for (chat in chats) {
        contact = document.createElement("div");
        contact.class = "contact";
        contact.id = chats[chat];
        view_contact = document.createElement("div");
        view_contact.class = "view_contact";

        img = document.createElement("img");
        img.alt = "logo";
        img.class = "logo";

        img.src = await get_avatar_url_by_id(chats[chat].ids[0]);

        name_contact = document.createElement("p");
        name_contact.class = "name_contact";
        name_contact.textContent = chats[chat];

        view_contact.append(img, name_contact);
        view_message = document.createElement("div");
        view_message.class = "view_message";
        view_message.textContent = chats[chat][nickname]; // Добавить ссылку из бд
        contact.append(view_contact, view_message);
        contacts.append(contact);
    }

    document.getElementById('chat_for_oponent').scrollIntoView(true);
}

async function get_avatar_url_by_id(id) {
    const response = await fetch(
        "http://localhost/data/user/",
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "users_ids": [id]
            })
        }
    );

    if (response.status == 200) {
        const data = await response.json();
        return data[0].avatar_url;
    }
}

async function create_chat(oponents_id) {
    await fetch(('http://127.0.0.1/data/chats/add/'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "members": oponents_id
        })
    });
    await load_contacts();
}


async function send_message(chat_id) {
    let input = document.getElementById("send_message");
    let message = input.textContent;
    input.textContent = "";
    let user_id = localStorage.getItem("id");
    await fetch(('http://127.0.0.1/data/messages/' + chat_id), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: {
            "chat_id": chat_id,
            "content": message,
            "sender": user_id
        }
    });
}
