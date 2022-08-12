import glob
import os.path
import re
import subprocess
import sys
from typing import Optional

import PyPDF2


def main(argv: list):
    for path in glob.glob(argv[1]):
        print('-' * 30)
        print(os.path.basename(path))
        print('doi: %s' % get_doi(path))


def get_doi(path: str) -> Optional[str]:
    meta_data = get_pdf_meta_data(path)
    print(meta_data)

    doi_keys = ['/doi', '/DOI', '/Doi', '/WPS-ARTICLEDOI', '/prism:doi']
    for key in doi_keys:
        if key in meta_data:
            print('from doi in meta data')
            return meta_data[key]

    if '/Subject' in meta_data:
        doi = extract_doi(meta_data['/Subject'])
        if doi is not None:
            print('from subject in meta data')
            return doi

    doi = extract_doi(extract_text(path))
    if doi is not None:
        print('from text')
        return doi

    return None


def get_pdf_meta_data(path: str) -> dict:
    pdf = PyPDF2.PdfFileReader(path)
    return pdf.documentInfo


def extract_doi(s: str) -> Optional[str]:
    m = re.search(r'doi:(\S+)', s, flags=re.IGNORECASE)
    if m:
        return m[1]
    else:
        return None


def extract_text(path: str) -> str:
    return subprocess.check_output(['pdf2txt.py', path]).decode('utf-8')


if __name__ == '__main__':
    main(sys.argv)
