'use strict';

// ############################## Index ##############################

const createReportTableRow = function(report) {
  // Create a HTML table row from the report object.
  const tableRow = $('<tr>');
  tableRow.append('<td>' + report.report_id + '</td>');
  tableRow.append('<td>' + report.category + '</td>');
  tableRow.append('<td>' + report.original_language + '</td>');
  tableRow.append('<td>' + report.creation_date + '</td>');
  if (report.processed === true) {
    tableRow.append('<td><span class="glyphicon glyphicon-thumbs-up gi-2x"></span></td>');
  } else {
    tableRow.append('<td><span class="glyphicon glyphicon-thumbs-down gi-2x"></span></td>');
  }

  const hyperlinkReport = $('<a href="/report/' + report.report_id + '">');
  hyperlinkReport.append('<span class="glyphicon glyphicon-book gi-2x"></span>');
  const hyperlinkColumn = $('<td>').append(hyperlinkReport);
  tableRow.append(hyperlinkColumn);

  return tableRow;
};

const addRowToReportTable = function(row) {
  const rows = $('#last-reports-table tbody tr');

  if (rows.length === 10) {
    rows.last().remove();
  }

  $('#last-reports-table tbody').prepend(row);
};

const addReportToReportTable = function(report) {
  const newRow = createReportTableRow(report);
  addRowToReportTable(newRow);
};

// ############################## Report ##############################

/** This makes that the popovers disappear when the user clicks outside of the popover.
 *  Found somewhere on Stackoverflow
 */
const closePopoverOnOuterClick = function() {
  $(document).on('click', function (e) {
    $('[data-toggle="popover"],[data-original-title]').each(function () {
      //the 'is' for buttons that trigger popups
      //the 'has' for icons within a button that triggers a popup
      if (!$(this).is(e.target) && $(this).has(e.target).length === 0 &&
           $('.popover').has(e.target).length === 0) {
          (($(this).popover('hide').data('bs.popover')||{}).inState||{}).click = false;
      }
    });
  });
};

/*
 * Creates the content of the popover from a list of the annotated classes
 *
 * The popover will contain a carousel in which each slide is one of the annotations with
 * which a certain words was annotated.
 */
const popoverContent = function(annotatedClasses) {

  const carousel = $('<div>', {
    'id': 'popover-carousel',
    'class': 'carousel',
    'data-interval': false,
  });

  const carouselInner = $('<div class="carousel-inner" role="listbox">');
  carousel.append(carouselInner);

  // Create a carousel slide for each of the annotations for that word.
  $.each(annotatedClasses, function(j, annotatedClass) {

    const termSynonyms = annotatedClass.synonym;
    const termDefinition = annotatedClass.definition;
    const termPrefLabel =  annotatedClass.prefLabel;
    const termUrl = annotatedClass['@id'].replace('#', '');

    const carouselItem = $('<div class="item">');
    // Only one of the slides can be active.
    if (j === 0) {
      carouselItem.addClass('active');
    }

    // Each slide of the carousel consists of a panel
    const panel = $('<div class="panel panel-default popover-panel">');

    const panelHeading = $('<div class="panel-heading">');
    panelHeading.text(termPrefLabel.toTitleCase());

    const panelBody = $('<div class="panel-body">');

    if (termDefinition.length > 0) {
        panelBody.append(termDefinition);
    } else {
        panelBody.append('No definition available.');
    }

    panelBody.append($('<br><br>'));

    if (termSynonyms.length > 0) {
      const synonymsDiv = $('<div class="popover-synonyms">');
      synonymsDiv.append($('<b>Synonyms: </b>'));
      let synonymsDivText = '';
      $.each(termSynonyms, function(i, synonym) {
        if (i !== 0) {
          synonymsDivText += ', ';
        }
        synonymsDivText += synonym;
      });
      synonymsDiv.append(synonymsDivText);
      panelBody.append(synonymsDiv);
      panelBody.append($('<br>'));
    }

    const infoButton = $('<a>', {
      'target': '_blank',
      'href': termUrl,
      'class' : 'btn btn-primary btn-popover',
      'type': 'button',
      text: 'Click for more information',
    });

    panelBody.append(infoButton);

    // Only add arrows if there is more than one slider
    if (annotatedClasses.length > 1) {
      const arrowsDiv = $('<div id="popover-arrows">');

      const leftArrow = $('<a>', {
        'class': 'left carousel-control',
        'href': '#popover-carousel',
        'data-slide': 'prev',
        'role': 'button',
      }).append($('<span>', {
        'class': 'glyphicon glyphicon-arrow-left popover-arrow',
        'aria-hidden': true,
      }));

      const rightArrow = $('<a>', {
        'class': 'right carousel-control',
        'href': '#popover-carousel',
        'data-slide': 'next',
        'role': 'button',
      }).append($('<span>', {
        'class': 'glyphicon glyphicon-arrow-right popover-arrow',
        'aria-hidden': true,
      }));

      arrowsDiv.append(leftArrow, rightArrow);
      panelHeading.append(arrowsDiv);
    }

    panel.append(panelHeading, panelBody);
    carouselItem.append(panel);
    carouselInner.append(carouselItem);
  });

  return carousel[0].outerHTML;
};

// From a list of annotations and a list of words, create a annotated text.
const annotateTranslatedText = function(annotations, splitTextToAnnotate) {

  // This will be equivalent to splitTextToAnnotate, but will contain annotated words.
  const splitAnnotatedText = [];

  $.each(splitTextToAnnotate, function(i, token) {

    let tokenText = token[0];
    const tokenFrom = token[1];
    const tokenTo = token[2];
    // Classes with which this token is annotated
    const annotatedClasses = [];

    $.each(annotations, function(j, term) {
      const annotatedClass = term.annotatedClass;
      $.each(term.annotations, function(j, annotation) {
        // If the annotation begins in the beginning of the word or ends where the word ends,
        // it means that the word is annotated
        if (annotation.from === tokenFrom + 1 || annotation.to === tokenTo + 1) {
          // To avoid repetition of annotations. This would happen if a word is annotated with a
          // certain class and a longer expression which includes that word is annotated with the
          // same class. For example, both "Supraspinatus" and "Supraspinatus Muscle" are annotated
          // with the "supraspinatus muscle" class.
          if (annotatedClasses.indexOf(annotatedClass) === -1) {
            annotatedClasses.push(annotatedClass);
          }
        }
      });
    });

    if (annotatedClasses.length > 0) {
      const annotButton = $('<a>', {
        'class': 'btn btn-default',
        'id': 'annotation',
        'data-content': popoverContent(annotatedClasses),
        'data-toggle': 'popover',
        'data-placement': 'bottom auto',
        'data-viewport': '#reports-tab-content',
        text: tokenText
        });
      // Updates the token text with the annotated version
      tokenText = annotButton[0].outerHTML;
    }

    splitAnnotatedText.push(tokenText);

  });

  const annotatedText = splitAnnotatedText.join('');
  return annotatedText;
};
