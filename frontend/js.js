function sign_in_account() {
    if (document.getElementsByClassName("main").item(0).id == "main_sign_in"){
        let username = document.getElementById("input_username").value;
        let password = document.getElementById("input_password").value;
        if (password.length >= 8) {
            if (password.toLowerCase() != password) {
                if (password.toUpperCase() != password) {
                            error_text.textContent = "";
                            login(username, password)//TODO отправлять на эндпоинт для авторизации(:8000/auth), принимать jwt токены(refresh и access) и сохранять их в localStorage 
                }else {error_text.textContent = "Нету символа(ов) нижнего регистра в пароле"}
            }else {error_text.textContent = "Нету символа(ов) верхнего регистра в пароле"}
        } else {error_text.textContent = "Длина пароля меньше 8"}
        
    }
    else {create_sign_in_container()}
}



function registration_account() {
    if (document.getElementsByClassName("main").item(0).id == "main_registration"){
        let username = document.getElementById("input_username").value;
        let email = document.getElementById("input_email");
        let password = document.getElementById("input_password").value;
        let password_confirmation = document.getElementById("confirmation_input_password").value;
        if (password.length >= 8) {
            if (password.toLowerCase() != password) {
                if (password.toUpperCase() != password) {
                    if (password == password_confirmation) {
                        if (email.checkValidity()) {
                            console.log(username, email.value, password)
                            error_text.textContent = ""
                        } else {error_text.textContent = "Электронная почта не валидна"}       
                    } else {error_text.textContent = "Пароли не совпадают"}
                }else {error_text.textContent = "Нету символа(ов) нижнего регистра в пароле"}
            }else {error_text.textContent = "Нету символа(ов) верхнего регистра в пароле"}
        } else {error_text.textContent = "Длина пароля меньше 8"}
    }
    else {create_registration_container()}
}


function create_sign_in_container() {
    parent = document.getElementsByClassName("main").item(0).parentNode;
    new_main_div = document.createElement("div");
    new_main_div.id = "main_sign_in";
    new_main_div.className = "main";
    parent.insertBefore(new_main_div, document.getElementsByClassName("main").item(0));
    parent.removeChild(document.getElementsByClassName("main").item(1));

    header = document.getElementById("header")
    header.textContent = "Вход"

    error_h = document.createElement("h1");
    error_h.id = "error";

    username_input = document.createElement("input");
    username_input.type = "text";
    username_input.id = "input_username";
    username_input.className = "entry"
    username_input.placeholder = "Username";

    password_input = document.createElement("input");
    password_input.type = "password";
    password_input.id = "input_password";
    password_input.className = "entry"
    password_input.placeholder = "Password";
    password_input.autocomplete = "current-password";

    reset_password_btn = document.createElement("p");
    reset_password_btn.id = "reset_password";
    reset_password_btn.textContent = "Забыл пароль?";

    sign_in_btn = document.createElement("input");
    sign_in_btn.type = "button";
    sign_in_btn.id = "sign_in";
    sign_in_btn.className = "active btn"
    sign_in_btn.value = "Войти";

    registration_btn = document.createElement("p");
    registration_btn.id = "registration";
    registration_btn.className = "btn"
    registration_btn.textContent = "Зарегистрироваться";

    new_main_div.append(error_h, username_input, password_input, reset_password_btn, sign_in_btn, registration_btn);
    activate_btn();
}

function create_registration_container() {
    parent = document.getElementsByClassName("main").item(0).parentNode;
    new_main_div = document.createElement("div");
    new_main_div.id = "main_registration";
    new_main_div.className = "main";
    parent.insertBefore(new_main_div, document.getElementsByClassName("main").item(0));
    parent.removeChild(document.getElementsByClassName("main").item(1));

    header = document.getElementById("header")
    header.textContent = "Регистрация"

    error_h = document.createElement("h1");
    error_h.id = "error";

    username_input = document.createElement("input");
    username_input.type = "text";
    username_input.id = "input_username";
    username_input.className = "entry"
    username_input.placeholder = "Username";

    email_input = document.createElement("input");
    email_input.type ="email";
    email_input.id = "input_email";
    email_input.className = "entry"
    email_input.placeholder = "E-mail";

    password_input = document.createElement("input");
    password_input.type = "password";
    password_input.id = "input_password";
    password_input.className = "entry"
    password_input.placeholder = "Password";
    password_input.autocomplete = "new-password";

    password_confirmation_input = document.createElement("input");
    password_confirmation_input.type = "password";
    password_confirmation_input.id = "confirmation_input_password";
    password_confirmation_input.className = "entry"
    password_confirmation_input.placeholder = "Confirmation password";
    password_confirmation_input.autocomplete = "new-password";

    sign_in_btn = document.createElement("p");
    sign_in_btn.id = "sign_in";
    sign_in_btn.className = "btn"
    sign_in_btn.textContent = "Войти в аккаунт";

    registration_btn = document.createElement("input");
    registration_btn.type = "button";
    registration_btn.id = "registration";
    registration_btn.className = "active btn"
    registration_btn.value = "Зарегистрироваться";

    new_main_div.append(error_h, username_input, email_input, password_input, password_confirmation_input, registration_btn, sign_in_btn);
    activate_btn();
}

function activate_btn() {
    registration = document.getElementById("registration");
    sign_in = document.getElementById("sign_in");
    error_text = document.getElementById("error");

    sign_in.addEventListener("click", sign_in_account);
    registration.addEventListener("click", registration_account);
}