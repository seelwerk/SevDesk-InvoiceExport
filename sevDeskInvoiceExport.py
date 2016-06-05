#!/usr/bin/env python
import os
import json
import logging
from dateutil.parser import parse
from urllib2 import Request, urlopen, URLError, HTTPError
from optparse import OptionParser

options = OptionParser(usage='%prog [options]', description='Tool to backup all Invoices from SevDesk')
options.add_option('-t', '--apitoken', help='Api Token for SevDesk.de API')
options.add_option('-f', '--folder', help='Folder where to put the files, default=current dir')

logging.basicConfig(filename='backupInvoices.log', level=logging.INFO, format='%(asctime)s %(message)s')


SEVDESK_API = 'https://my.sevdesk.de/api/v1/'


def get_invoice_pdf(invoice_id, filepath):
    url = SEVDESK_API + 'Invoice/%s/getPdf/?download=1' % invoice_id
    try:
        request = Request(url, headers=headers)
        f = urlopen(request)
        logging.debug("downloading " + url)

        with open(filepath, "wb+") as local_file:
            local_file.write(f.read())

    except HTTPError, e:
        logging.error("HTTP Error:", e.code, url)
    except URLError, e:
        logging.error("URL Error:", e.reason, url)


def get_invoicing_details():
    request = Request(SEVDESK_API + 'Invoice/?limit=100&offset=0&embed=embed', headers=headers)
    json_response = json.loads(urlopen(request).read())
    return json_response['objects']


def main():
    opts, args = options.parse_args()
    if not opts.apitoken:
        options.error('ApiToken missing')

    # Define Headers, valid for all requests
    global headers
    headers = {
        'Authorization': opts.apitoken,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    if not opts.folder:
        base = os.path.dirname(os.path.realpath(__file__))
    else:
        if not opts.folder.startswith("/"):
            base = base = os.path.dirname(os.path.realpath(__file__)) + "/" + opts.folder
        else:
            base = opts.folder

    logging.info("Receiving invoicing list from SevDesk")
    invoices = get_invoicing_details()

    for invoice in invoices:
        invoice_id = invoice['id']
        invoice_number = invoice['invoiceNumber']

        # Get Year of Invoice
        dt = parse(invoice['invoiceDate'])
        invoice_year = dt.strftime('%Y')

        # Create directory
        year_directory = os.path.join(base, str(invoice_year) + "/")
        try:
            os.makedirs(year_directory)
        except Exception, e:
            pass

        # Get Invoice if not existing
        filename = invoice_number + ".pdf"
        invoice_path = os.path.join(year_directory, filename)
        if os.path.isfile(invoice_path) is False:
            logging.info("Getting Invoice: " + invoice_number)
            get_invoice_pdf(invoice_id, invoice_path)

    logging.info("Finished processing")


if __name__ == '__main__':
    main()
