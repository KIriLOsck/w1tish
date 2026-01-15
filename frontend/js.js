const main_div = document.getElementById("main");
const registration = document.getElementById("registration");
const sign_in = document.getElementById("sign_in");
sign_in.addEventListener("click", sign_in_account);
registration.addEventListener("click", registration_account);
function sign_in_account() {
    if (main_div.className == "main_sign_in"){
        let username = document.getElementById("input_username").value;
        let password = document.getElementById("input_password").value;
        console.log(username, password);
    }
    else {
        parent = main_div.parentNode;
        new_main_div = document.createElement("div")
        new_main_div.id = "main"
        new_main_div.className = "main_sign_in"
        parent.insertBefore(new_main_div, main_div)
        parent.removeChild(main_div)
        username_input = document.createElement("input")
        username_input.type = "text"
        username_input.id = "input_username"
        username_input.placeholder = "Имя пользователя"
        password_input = document.createElement("input")
        password_input.type = "text"
        password_input.id = "input_password"
        password_input.placeholder = "Пароль"
        sign_in_btn = document.createElement("input")
        sign_in_btn.type = "button"
        sign_in_btn.id = "sign_in"
        sign_in_btn.value = "Войти в аккаунт"
        registration_btn = document.createElement("input")
        registration_btn.type = "button"
        registration_btn.id = "registration"
        registration_btn.value = "Зарегистрироваться"
        new_main_div.append(username_input, password_input, sign_in_btn, registration_btn)

    }
}

function registration_account() {
    if (main_div.className == "main_registration"){
        let username = document.getElementById("input_username")
        let email = document.getElementById("input_email")
        let password = document.getElementById("input_password")
        let password_confirmation = getElementById("input_password_confirmation")
        if (length(password) >= 8) {
            if (password.toLowerCase() != password) {
                if (password.toUpperCase() != password) {
                    if (password == password_confirmation) {
                        console.log(username, email, password)
                    }
                }
            }
        } 
    }
    else {
        parent = main_div.parentNode;
        new_main_div = document.createElement("div")
        new_main_div.id = "main"
        new_main_div.className = "main_registration"
        parent.insertBefore(new_main_div, main_div)
        parent.removeChild(main_div)
        username_input = document.createElement("input")
        username_input.type = "text"
        username_input.id = "input_username"
        username_input.placeholder = "Имя пользователя"
        email_input = document.createElement("input")
        email_input.type = "text"
        email_input.id = "input_email"
        email_input.placeholder = "E-mail"
        password_input = document.createElement("input")
        password_input.type = "text"
        password_input.id = "input_password"
        password_input.placeholder = "Пароль"
        sign_in_btn = document.createElement("input")
        sign_in_btn.type = "button"
        sign_in_btn.id = "sign_in"
        sign_in_btn.value = "Войти в аккаунт"
        registration_btn = document.createElement("input")
        registration_btn.type = "button"
        registration_btn.id = "registration"
        registration_btn.value = "Зарегистрироваться"
        new_main_div.append(username_input, email_input, password_input, registration_btn, sign_in_btn)
    }
}
