'use strict';

jQuery(document).ready(function($) {

  const textDiv = $('#annotated_text');

  if (annotations !== null) {
    // The arguments given to the function are defined in the HTML, received from Jinja
    const annotatedText =  annotateTranslatedText(annotations, splitTextToAnnotate);
    const annotatedTextProcessed = annotatedText.replace(/\n/g, '<br>');
    textDiv.html(annotatedTextProcessed);
  } else {
    textDiv.html('Report was not yet annotated.');
  }

  $('[data-toggle=popover]').popover({'html': true, 'trigger': 'click'});
  closePopoverOnOuterClick();

});
