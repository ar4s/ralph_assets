(function(){
    "use strict";

    var Bulk = function () {};

    var toggleChildDisplay = function() {
        var trigger = this;
        var trgt_id = $(trigger).attr('data-trgt');
        if (trgt_id.length === 0) {
            throw {
                'name': "TargetNotSpecified",
                'description': "Attribute 'data-trgt' not specified.",
            };
        }
        var threshold = $(trigger).attr('data-threshold') || 5;
        var targets = $('#' + trgt_id).children().slice(threshold);
        $(targets).each(function(idx, trgt) {
            $(trgt).toggle();
        });

        // swap button text msg
        var currentMsg = $(trigger).text();
        var altMsg = $(trigger).attr('data-alt-msg');
        $(trigger).attr('data-alt-msg', currentMsg);
        $(trigger).text(altMsg);
    };

    Bulk.prototype.get_ids = function(){
        var ids = [];
        $("#assets_table input[type=checkbox]").each(
            function(index, val){
                if(val.checked) {
                    ids.push($(val).val());
                }
            }
        );
        return ids;
    }

    Bulk.prototype.edit_selected = function() {
        var ids = this.get_ids();
        if (ids.length) {
            window.location.href = 'bulkedit?select=' + ids.join('&select=');
        }
        return false;
    };

    Bulk.prototype.invoice_report_selected = function() {
        var ids = this.get_ids();
        if (ids.length){
            window.location.href = 'invoice_report?select=' + ids.join('&select=');
        }
    };

    Bulk.prototype.invoice_report_search_query = function () {
        var params = window.location.search;
        if (params.length){
            window.location.href = 'invoice_report' + params + '&from_query=1';
        }
    };

    Bulk.prototype.addAttachment = function(type) {
        var ids = this.get_ids();
        if (ids.length){
            window.location.href = 'add_attachment/' + type + '/?select=' + ids.join('&select=');
        }
    };

    Bulk.prototype.transition_selected = function(type) {
        var ids = this.get_ids();
        var params = window.location.search;
        var selected_all_pages = $('.selected-assets-info-box').data('selected');

        if (selected_all_pages &&
            params.length &&
            $.inArray(type, ['release-asset', 'return-asset', 'loan-asset']) != -1
        ) {
             window.location.href = 'transition' + params + '&from_query=1&transition_type=' + type;
        } else if (
            ids.length &&
            $.inArray(type, ['release-asset', 'return-asset', 'loan-asset']) != -1
        ) {
            window.location.href = 'transition?select=' + ids.join('&select=') + '&transition_type=' + type;
        }
    };

    Bulk.prototype.append_bob_select_item = function() {
        // append item to select on all pages
        if ($('[data-searched-items]').data('searched-items') && $('.pagination li').length > 1 ){
            var item = $('.select-all-pages');
            var new_item = item.clone();
            item.remove();
            $('#assets_table .dropdown .dropdown-menu'  ).prepend(new_item);
            new_item.show();
        }
    }

    Bulk.prototype.select_all_pages = function() {
        var selected_box = $('.selected-assets-info-box');
        var selected_all_pages = selected_box.data('selected');

        $('.bob-select-all-pages i').toggleClass('fugue-blue-documents-stack fugue-documents-stack');
        $('.bob-select-all-pages span').toggle();
        $(selected_box).toggle();
        selected_all_pages = !selected_all_pages;
        selected_box.data('selected', selected_all_pages);
        if (selected_all_pages){
            $(".bob-select-all").trigger("click");
        } else {
            $(".bob-select-none").trigger("click");
        }
    };

    $(document).ready(function() {
        var bulk = new Bulk();
        $('#post_edit_all').click(function() {
            bulk.edit_selected();
        });
        $('#post_invoice_report_selected').click(function() {
            bulk.invoice_report_selected();
        });
        $('#post_invoice_report_search_query').click(function() {
            bulk.invoice_report_search_query();
        });

        $(" #post_release_transition_selected, \
            #post_return_transition_selected, \
            #post_loan_transition_selected \
        ").click(function() {
            var type = $(this).data('transition-type');
            bulk.transition_selected(type);
        });

        $('#post_add_attachment').click(function() {
            bulk.addAttachment('asset');
        });

        $('.delete-attachment').click(function() {
            if (!confirm("Are you sure to delete Attachment(s)?")) {
                return false;
            }
            var delete_type = $(this).attr('data-delete-type');
            var form_id = '#' + $(this).attr('data-form-id');
            $(form_id).find("input[name='delete_type']").val(delete_type);
            $(form_id).submit();
        });

        $('.del-asset-btn').click(function() {
            if (!confirm("Are you sure to delete Asset?")) {
                return false;
            }
        });
        require(['reports'], function(reports) {
            reports.setup({
                trigger: $('.pagination').find('a').last(),
                progressBar: '#async-progress',
                etaEl: '#eta'
            });
        });

        bulk.append_bob_select_item();

        $('.bob-select-all-pages').click(function() {
            bulk.select_all_pages();
        });

        // set status as 'in progress' if user is selected
        $("#id_user").change(function() {
            if($(this).val() !== "") {
                $('#id_status option').filter(function () {
                    return $(this).text() == 'in progress';
                }).prop('selected', true);
            }
        });

        $('.toggle-child-display').click(toggleChildDisplay);
    });

})();
