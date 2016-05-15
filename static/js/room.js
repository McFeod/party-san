$(function(){
    $('.choices > div').each(function(i, elem){
        highlight_choices(elem)
    });
});


function highlight_choices(btn_group){
    var buttons = $(btn_group).children();
    buttons.removeClass("btn-default btn-primary btn-danger btn-success");
    var next_classes = [
            ["btn-default", "btn-default", "btn-default"],
            ["btn-danger", "btn-default", "btn-default"],
            ["btn-default", "btn-primary", "btn-default"],
            ["btn-default", "btn-default", "btn-success"]
    ];
    jQuery.map(next_classes[$(btn_group).data("selected")], function(new_class, i){
        buttons.eq(i).addClass(new_class);
    })
}


function choice_click(elem, num){
    var parent = $(elem).parent();
    parent.data("selected", num);
    $.ajax({
        url: ANSWER_URL,
        data: {'choice': num,
               'type': parent.data("type"),
               'id': parent.data("id")
              },
        // success: function(data){
        //     alert(data)
        // }
    });
    highlight_choices(parent);
}


function description_click(elem){
    if ($(elem).hasClass("entry_description_short")){
        $(elem).removeClass("entry_description_short").addClass("entry_description_long");
        $(elem).children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
    } else  {
        $(elem).removeClass("entry_description_long").addClass("entry_description_short");
        $(elem).children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
    }
}


function add_from_modal(form_selector, validator) {
    if (change_from_modal(form_selector, validator))
        $(form_selector)[0].reset();
}

function change_from_modal(form_selector, validator) {
    validator = validator || dummy_validator;
    var form = $(form_selector);
    if (validator(form)) {
        form.submit();
        form.find('p').html("");
        $(form_selector).closest(".modal").modal("hide");
        return true;
    }
    return false;
}


function reset_submit(form_selector){
    var frm = $(form_selector);
    frm.submit(function (ev) {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize()
        });
        ev.preventDefault();
    });
}


function show_new_widget(data) {
    var beginning = `
    <div class="row entry">
        <div class="btn btn-default entry_description_short col-xs-9">
            <p class="text-left">
                ${data.description}
            </p>
            <i class="fa fa-angle-down spoiler" onclick="description_click(this.closest('div'))"></i>`;
    var admin = `
        <div class="admin_options">
            <button class="admin_option edit_option" onclick="edit_option_dialog(${data.option_id}, this)"><i class="fa fa-edit"></i></button>
            <button class="admin_option remove_option" onclick="remove_option_dialog(${data.option_id}, this)"><i class="fa fa-trash"></i></button>
        </div>`;
    var ending = `
        </div>
        <div class="choices col-xs-3">
            <div class="btn-group btn-group-lg" role="group" data-selected="0" data-type="possibility" data-id="${data.option_id}">
                <button type="button" class="btn btn-default" onclick="choice_click(this, 1)"><i class="fa fa-times-circle"></i></button>
                <button type="button" class="btn btn-default" onclick="choice_click(this, 2)"><i class="fa fa-question-circle"></i></button>
                <button type="button" class="btn btn-default" onclick="choice_click(this, 3)"><i class="fa fa-check-circle"></i></button>
            </div>
            <br>
            <div class="btn-group btn-group-lg" role="group" data-selected="0" data-type="rating" data-id="${data.option_id}">
                <button type="button" class="btn btn-default" onclick="choice_click(this, 1)"><i class="fa fa-frown-o"></i></button>
                <button type="button" class="btn btn-default" onclick="choice_click(this, 2)"><i class="fa fa-meh-o"></i></button>
                <button type="button" class="btn btn-default" onclick="choice_click(this, 3)"><i class="fa fa-smile-o"></i></button>
            </div>
        </div>
    </div>`;
    if (IS_ADMIN || (data.author_id == USER_ID))
        $("#options").append(beginning + admin + ending);
    else
        $("#options").append(beginning + ending);
}


function disable_widget(data){
    $(`[data-id=${data.option_id}]>button`)
        .attr("disabled", "disabled")
        .closest(".row.entry").find("p").html("[УДАЛЕНО]")
        .closest("div").find("button").attr("disabled", "disabled")
}


function change_widget(data){
    $(`[data-id=${data.option_id}]`).closest(".row").find("p").html(data.description);
}


function handle_scenario(data){
    var handlers = {
        "add": show_new_widget,
        "remove": disable_widget,
        "change": change_widget
    };
    handlers[data.command](data);
}


function edit_option_dialog(option_id, description) {
    var form = $('#edit_form');
    form.find('[name="description"]').val(get_description(description));
    form.find('[name="option_id"]').val(option_id);
    form.find('[name="option_type"]').val(TYPE);
    $('#edit_scenario_modal').modal();
}

function remove_option_dialog(option_id, description) {
    var form = $('#delete_form');
    form.find('p').html(get_description(description));
    form.find('[name="option_id"]').val(option_id);
    form.find('[name="option_type"]').val(TYPE);
    $('#delete_scenario_modal').modal();
}


function get_description(button) {
    return $.trim($(button).closest('.entry_description_short').find('p').html());
}


function dummy_validator(form){
    return true;
}

function empty_description(form) {
    if (!form.find('[name="description"]').val()){
        form.find('p').html("Поле не может быть пустым");
        return false;
    }
    return true;
}

function correct_passwords(form) {
    function show_error(msg) {
        form[0].reset();
        form.find('p').html(msg);
    }
    var p1 = form.find('[name="password1"]').val();
    var p2 = form.find('[name="password2"]').val();
    if (!p1){
        show_error("Пароль не может быть пустым!");
        return false;
    }
    else if (p1 != p2){
        show_error("Пароли не совпадают!");
        return false
    }
    return true;
}

function empty_time(form){
    if (!form.find('[name="description"]').val() && !form.find('[name="time"]').val()){
        form.find('p').html("Заполните хотя бы одно из полей");
        return false;
    }
    return true;
}