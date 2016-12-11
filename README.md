# sevDesk Invoice-Exporter
This python script is used to download all Invoices from SevDesk API and saves them in a local directory. So we can decouple our documents from SevDesk availability

### Usage
Clone this project, then:
```bash
# Make file executable
$ chmod +x sevDeskInvoiceExport.py

$ ./sevDeskInvoiceExport.py -t {YOUR-APITOKEN} [-f invoices/ ]
```
