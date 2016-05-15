function make_room(){
    var p1 = $('#passw1'), p2 = $('#passw2');
    if (p1.val() != p2.val()){
        p1.val("").attr("placeholder", "пароли").addClass("error");
        p2.val("").addClass("error").attr("placeholder", "не совпадают");
    }
    else{
        $('#new_room_form').submit();
    }
}
