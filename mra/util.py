import re


def split_span(s):
    tokens = []
    for match in re.finditer(r"[\w\d]+|[^\w\d\s]+|\s+", s):
        span = match.span()
        tokens.append((match.group(0), span[0], span[1] - 1))
    return tokens


def process_bioportal_annotations(annotations, bioportal_api):

    # Only want RadLex annotations
    radlex_annotations = filter(
        lambda annotation: 'radlex' in annotation['annotatedClass']['@id'],
        annotations
    )

    for annotation in radlex_annotations:

        # Get more information about the terms annotated
        cls_id = annotation['annotatedClass']['@id']
        class_info = bioportal_api.ontology_class('RADLEX', cls_id)
        for parameter in [u'prefLabel', u'synonym', u'obsolete', u'definition']:
            annotation['annotatedClass'][parameter] = class_info[parameter]

        # Delete information not needed
        del annotation['mappings']
        del annotation['hierarchy']
        info_to_keep = ['definition', 'synonym', 'obsolete', '@id', 'prefLabel']
        for key in annotation['annotatedClass'].keys():
            if key not in info_to_keep:
                del annotation['annotatedClass'][key]

    return radlex_annotations
