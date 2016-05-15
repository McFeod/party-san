function enter_room(){
    var room_field = $("#enter_room_number");
    if (!(parseInt(room_field.val())>0)){
        room_field.addClass("error").val("");
        $("#room_password").val("")
    } else {
        var frm = $("#enter_room_form");
        frm.attr("action", "/room/"+room_field.val()+"/enter/");
        frm.submit()
    }
}