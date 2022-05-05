function show_hide_password(target){
    var input = target.parentElement.children[0];
    if (input.getAttribute('type') == 'password') {
        input.setAttribute('type', 'text');
    } else {
        input.setAttribute('type', 'password');
    }
    return false;
}