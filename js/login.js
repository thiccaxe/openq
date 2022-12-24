import * as api from "/js/api.js"

api.retrieve_default_endpoint(true);

var password_input, username_input, login_form;

function toggle_visibility() {
  if (password_input.type == "password") {
    password_input.type = "text";
  } else {
    password_input.type = "password";
  }
}

function login_callback(r) {
  let data = JSON.parse(r.responseText);
  if ((r.status+"")[0] != 2) {
    
  }
  else {
    
  }
}

function submit_login(){
  let password = password_input.value;
  let username = username_input.value;
  
  api.login(username, password, login_callback)
  
  return false;
}

window.onload = function() {
  password_input = document.getElementById("password_input");
  username_input = document.getElementById("username_input");
  login_form = document.getElementById("login_form");
  
  login_form.onsubmit = submit_login;
}