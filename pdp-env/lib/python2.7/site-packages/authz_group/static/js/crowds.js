(function($) {
    var compiled_templates = {};

    $.fn.crowd_control = function(options) {
        var opts = $.extend( { group_ids: [] }, options);

        return this.each(function() {
            initialize_crowds($(this), opts);
        });
    };

    function handle_cc_click(ev) {
        var target_class = ev.target.className;

        if (target_class == "cc_cancel") {
            cancel_chooser($(this));
        }
        else if (target_class == "cc_save") {
            save_chooser($(this));
        }
        else if (target_class == "cc_remove_crowd") {
            remove_preselected_crowd(ev.target);
        }
        else if (target_class == "cc_readd_crowd") {
            readd_preselected_crowd(ev.target);
        }
        else if (target_class == "cc_show_full_chooser") {
            show_full_crowd_chooser($(this));
        }
        else if (target_class == "cc_crowd_filter_source_type") {
            filter_group_display_by_source($(this), ev.target.rel);
        }
    }

    function filter_group_display_by_source(instance, filter) {
        if (filter == 'all') {
            instance.find(".cc_crowd").show();
            return;
        }

        instance.find(".cc_crowd").hide();
        instance.find(".cc_crowd."+filter).show();
    }

    function show_full_crowd_chooser(instance) {
        var current_ids = get_selected_groups(instance);

        show_chooser(instance, {
            selected: current_ids,
            group_data: instance.data('group_data'),
            show_starting_selection: false
        });
    }

    function cancel_chooser(instance) {
        instance.trigger('cancel');
    }

    function save_chooser(instance) {
        var ids = get_selected_groups(instance);
        instance.trigger('save', [ids]);
    }

    function get_selected_groups(instance) {
        var checked = instance.find("div.cc_chooser_panel:visible input.cc_crowd_select:checked");
        var checked_len = checked.length;

        var ids = [];
        for (var i = 0; i < checked_len; i++) {
            ids.push($(checked[i]).val());
        }
        return ids;
    }

    function initialize_crowds(instance, opts) {
        instance.addClass("crowd_control");
        instance.addClass("cc_loading");
        instance.data('selected_groups', opts.group_ids);

        instance.on("click", handle_cc_click);

        $.ajax('/crowds/rest/v1/groups', {
            success: function(data) { group_data_success(instance, data); }
        });
    };

    function group_data_success(instance, data) {
        var crowds = data.crowds;
        instance.data('source_types', data.source_types);
        show_chooser(instance, {
            selected: instance.data()["selected_groups"],
            group_data: crowds,
            show_starting_selection: true
        });

        instance.removeClass("cc_loading");
    };

    function show_chooser(instance, opts) {
        var group_data = opts["group_data"];

        var len = group_data.length;

        var selected_groups = opts["selected"];
        var group_lookup = {};
        for (var i = 0; i < selected_groups.length; i++) {
            group_lookup[selected_groups[i]] = true;
        }

        instance.data('group_data', group_data);

        for (var i = 0; i < group_data.length; i++) {
            if (group_lookup[group_data[i].id]) {
                group_data[i].selected = true;
            }
            else {
                group_data[i].selected = false;
            }
        }

        var source_types = instance.data()['source_types'];
        var template_data = {
            has_selected_groups: (selected_groups.length && opts["show_starting_selection"]),
            crowds: group_data,
            source_types: source_types
        };

        var template = get_compiled_template("cc_group_list");

        instance.html(template(template_data));
    };

    function get_compiled_template(id) {
        if (!compiled_templates[id]) {
            var source = $("#"+id).html();
            var template = Handlebars.compile(source);
            compiled_templates[id] = template;
        }

        return compiled_templates[id];
    }

    function remove_preselected_crowd(target) {
        var containing_div = $(target).closest(".cc_crowd_wrapper");
        containing_div.addClass('cc_removed_crowd');
        containing_div.find("input").prop('checked', false);
    }
    function readd_preselected_crowd(target) {
        var containing_div = $(target).closest(".cc_crowd_wrapper");
        containing_div.removeClass('cc_removed_crowd');
        containing_div.find("input").prop('checked', true);
    }

}(jQuery));



