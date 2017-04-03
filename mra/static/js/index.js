'use strict';

jQuery(document).ready(function($) {

  $('#upload-report-form').ajaxForm(function(report) {
    addReportToReportTable(report);
    $('#upload-report-form')[0].reset();
    });

});
