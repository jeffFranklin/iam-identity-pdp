function cancel_handle(ev) {
    console.log("Cancel for: ", ev.target);
}

function save_handle(instance, ids) {
    console.log("Save for: ", $(instance).parent());
    console.log("IDS: ", ids);
}

$(".demo_panel1").crowd_control().on('cancel', cancel_handle).on('save', save_handle);


var ids = [];
for (var i = 0; i < 40; i++) {
    ids.push(i);
}

$(".demo_panel2").crowd_control({group_ids: ids }).on('cancel', cancel_handle).on('save', save_handle);

