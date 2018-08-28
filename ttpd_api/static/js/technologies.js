/*!
 * technologies.js
 * 
 * Copyright (c) 2017 Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
 * Licensed under MIT
 */

jQuery(document).ready(function($) {
    "use strict";

    var formCard = $('#form-card');
    var formTabs = $('#form-tabs');
    var protectionLevel = $('#id_protection_level');

    // [Protection Level Switch] ::start
    protectionLevel

        // bind event listener to the element
        .on('change.protection_level', function(evt) {
            var value = $(this)
                .children('option')
                .filter(':selected')
                .get(0)
                ;

            formCard.toggleClass('card--ip-protected', (value.innerText.toLowerCase() === 'ip protected'));
        })

        // trigger the event immediately on load.
        .trigger('change.protection_level')
        ;
    // [Protection Level Switch] ::end

    // [Show tabs on load] ::start
    (function() {
        var hash = window.location.hash;
        var prefix = 'form_tab--';

        // show tab onload only when the tab is not hidden
        if (hash) {
            formTabs
                .find('a[href="#' + hash.replace(prefix, '').split('#')[1] + '"]')
                .not(':hidden')
                .tab('show')
                ;
        }

        // replace the hash when changing tabs
        formTabs.find('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            window.location.hash = e.target.hash.replace("#", "#" + prefix);
        });
    })();
    // [Show tabs on load] ::end

    // [Reflect the selected filename on the custom file input] ::start
    (function() {
        $('form').on('change', '.custom-file-input', function (evt) {
            var fileInput = $(this);
            var files = fileInput.get(0).files;

            if (Object.keys(files).length === 0) {
                return;
            }

            fileInput
                .siblings('.custom-file-control')
                .data('selected-file', files[0].name)
                .attr('data-selected-file', files[0].name)
                ;
        })
    })();
    // [Reflect the selected filename on the custom file input] ::end

    // [Manage formset elements] ::start
    (function () {
        function generateElIdentifiers(index, prefix, suffix) {
            var name = prefix + '-' + index + '-' + suffix;

            return {
                name: name,
                id: 'id_' + name
            };
        }

        function createElements(conf) {
            var refEl  = conf.refEl;
            var subEls = ['path', 'description', 'DELETE'];
            var formElIdx = parseInt(conf.totalForms.val(), 10) - 1;

            // remove the classes
            conf.refEl.removeClass('inline-form-template d-none');

            // loop through all the subelements
            _.each(subEls, function(item) {
                var currentIdentifiers = generateElIdentifiers('__prefix__', conf.prefix, item);
                var nextIdentifiers    = generateElIdentifiers(formElIdx + 1, conf.prefix, item);

                // change the attributes for the label
                conf.refEl.find('label[for=' + currentIdentifiers.id + ']').attr('for', nextIdentifiers.id);

                // change the attributes for custom file control if present
                conf.refEl.find('.custom-file-control')
                    .attr('data-selected-file', 'Choose file...')
                    .data('selected-file', 'Choose file...')
                    ;

                // change the attributes for input element
                conf.refEl.find('#' + currentIdentifiers.id)
                    .attr('name', nextIdentifiers.name)
                    .attr('id', nextIdentifiers.id)
                    .val('')
                    ;
            });

            return {
                el: conf.refEl,
                idx: formElIdx + 1
            };
        }

        $('.card--asset-types')
            .on('click.create-entry', '.add-entry', function (evt) {
                var btn          = $(this);
                var parent       = btn.closest('.card--asset-types');
                var body         = parent.find('.card-body');
                var formTemplate = parent.find('.inline-form-template');
                var prefix       = formTemplate.data('form-el-prefix');

                var totalForms = $('#id_' + prefix + '-TOTAL_FORMS');
                var maxNumForms = $('#id_' + prefix + '-MAX_NUM_FORMS');

                // prevent the default behavior of the anchor
                evt.preventDefault();

                // show message when the total number of forms already reach the maximum
                if (totalForms.val() >= maxNumForms.val()) {
                    console.log('fuck overflow already!!!');
                    return;
                }

                // create the elements and append it
                var newElConf = createElements({
                    prefix: prefix,
                    totalForms: totalForms,
                    maxNumForms: maxNumForms,
                    refEl: formTemplate.first().clone()
                });

                // append it all once
                body.append(newElConf.el);

                // add border, margin, padding to the top of the element
                if (newElConf.el.siblings(':visible').length > 0) {
                    newElConf.el.addClass('inline-form-wrapper--bordered mt-3 pt-3');
                }

                // increment the number of forms in the formset
                totalForms.val(newElConf.idx + 1);

                // add disabled class to the button link
                if (totalForms.val() >= maxNumForms.val()) {
                    btn.addClass('disabled');
                }
            })

            // TODO: check and test the behavior thoroughly since we dont know if we should update the number of forms
            //       hidden field. Also show confirmation first before deleting it!
            .on('change.delete-entry', '.custom-control-input--delete', function (evt) {
                var checkbox = $(this);

                // do nothing when it is not checked
                if (!checkbox.prop('checked')) {
                    return;
                }

                var parent = checkbox.closest('.inline-form-wrapper');
                parent.fadeOut().promise().then(function() {
                    parent.addClass('d-none');
                });
            })
            ;
    })();
    // [Manage formset elements] ::end

});


