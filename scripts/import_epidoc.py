#!/usr/bin/env python3
"""Import a supplied EpiDoc edition without treating it as linguistic gold.

Keep the original bytes beside the JSON receipt: serialized XML fragments retain
element/attribute/text semantics, but are not a byte-exact replacement for XML.
"""
import argparse, hashlib, json, pathlib, re
import xml.etree.ElementTree as ET

TEI = 'http://www.tei-c.org/ns/1.0'
XMLID = '{http://www.w3.org/XML/1998/namespace}id'
UNITS = {'w', 'num', 'pc'}

def import_bytes(data, *, source_id, rights, locator):
    if not all(isinstance(x, str) and x.strip() for x in (source_id, rights, locator)):
        raise ValueError('source, rights and locator must be explicit')
    if len(data) > 16 * 1024 * 1024:
        raise ValueError('XML exceeds import size limit')
    # No entity expansion, remote resolution, DTDs or inferred identifiers.
    if re.search(br'<!\s*(DOCTYPE|ENTITY)\b', data, re.I) or b'\x00' in data:
        raise ValueError('DTD/entity declarations and non-UTF8 byte encodings rejected')
    root = ET.fromstring(data.decode('utf-8-sig'))
    if root.tag != '{'+TEI+'}TEI':
        raise ValueError('expected namespaced TEI root')
    seen = set()
    for element in root.iter():
        ident = element.get(XMLID)
        if ident is not None:
            if not ident.strip() or ident in seen:
                raise ValueError('empty or duplicate xml:id')
            seen.add(ident)
    editions = root.findall('.//{'+TEI+'}div[@type="edition"]')
    if len(editions) != 1:
        raise ValueError('exactly one edition required for an import receipt')
    edition = editions[0]
    parent = {child: element for element in edition.iter() for child in element}
    rows = []
    for element in edition.iter():
        if element.tag not in {'{'+TEI+'}'+name for name in UNITS}:
            continue
        ident = element.get(XMLID)
        if not ident:
            raise ValueError('text unit missing source-assigned xml:id')
        ancestor = parent.get(element)
        while ancestor is not None:
            if ancestor.tag in {'{'+TEI+'}'+name for name in UNITS}:
                raise ValueError('nested text units cannot be flattened into alignment')
            ancestor = parent.get(ancestor)
        # Only a plain, complete syllabic word has an unambiguous text view.
        simple = (element.tag == '{'+TEI+'}w' and len(element) == 0
                  and element.get('type') is None and element.get('part') is None
                  and element.get('cert') in (None, 'high'))
        rows.append({'source_unit_id': ident, 'unit_kind': element.tag.split('}')[-1],
                     'source_type': element.get('type'), 'attributes': dict(element.attrib),
                     'xml_fragment': ET.tostring(element, encoding='unicode'),
                     'complete_plain_syllabic_text': element.text if simple else None})
    if not rows:
        raise ValueError('edition has no identified text units')
    return {'format': 'epidoc-import-receipt-v1', 'source_id': source_id,
            'source_locator': locator, 'source_rights': rights,
            'source_xml_sha256': hashlib.sha256(data).hexdigest(), 'source_xml_bytes': len(data),
            'edition_xml': ET.tostring(edition, encoding='unicode'),
            'units': rows, 'annotation_groups_xml': [ET.tostring(e, encoding='unicode')
                for e in root.findall('.//{'+TEI+'}standOff')],
            'linguistic_gold': False, 'analyses_interpreted': False,
            'source_xml_must_be_retained': True,
            'boundary': 'Imported source encoding only; no schema certification, annotation interpretation, gold freeze or independent review.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('xml', type=pathlib.Path); p.add_argument('out', type=pathlib.Path)
    p.add_argument('--source-id', required=True); p.add_argument('--rights', required=True)
    p.add_argument('--locator', required=True)
    a = p.parse_args()
    result = import_bytes(a.xml.read_bytes(), source_id=a.source_id, rights=a.rights, locator=a.locator)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
