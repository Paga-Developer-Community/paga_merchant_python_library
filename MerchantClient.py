import requests
import hashlib
import json


def post_request(headers, json_data, url):
    response = requests.request(method="POST", url=url, headers=headers, data=json_data)
    return response


test_server = "https://qa1.mypaga.com/"
live_Server = "https://www.mypaga.com/"





class MerchantService(object):

    def __init__(self, principal, api_key, credential, test):
        self.principal = principal
        self.api_key = api_key
        self.credential = credential
        self.test = test

    def get_transaction_detail(self, reference_number):
        """ Get Transaction details

                Parameters
                ----------

                reference_number : string
                    reference_number The unique transaction code returned as part of a previously executed transaction
                Returns
                -------
                GetTransactionDetailResponse
                """
        endpoint = "paga-webservices/merchant-rest/secured/getTransactionDetails"
        data = {'referenceNumber': reference_number}

        pattern = reference_number + self.api_key

        print pattern

        hash = self.generateHash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text



    def get_transaction_details_by_invoice_number(self, invoice_number):
        """ Get Transaction details by invoice number

                Parameters
                ----------
                invoice_number : string
                    invoice_number The unique transaction code returned as part of a previously executed transaction
                Returns
                -------
                GetTransactionDetailsByInvoiceNumberResponse
                """
        endpoint = "paga-webservices/merchant-rest/secured/getTransactionDetailsByInvoiceNumber"
        data = {'invoiceNumber': invoice_number}

        pattern = invoice_number + self.api_key

        hash = self.generateHash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_process_details(self, process_code):
        """ Get Process details

                Parameters
                ----------
                process_code : string
                    process_code The process code returned as part of a previously executed transaction
                Returns
                -------
            GetProcessDetailsResponse
        """
        endpoint = "paga-webservices/merchant-rest/secured/getProcessDetails"
        data = {'processCode': process_code}

        print data

        pattern = process_code + self.api_key

        print pattern

        hash = self.generateHash(pattern)
        print hash

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_foreign_exchange(self, base_currency, foreign_currency):
        """ Get Foreign Exchange Rate

                  Parameters
                  ----------
                  base_currency : string
                      base_currency the originating currency code
                  foreign_currency : string
                      foreign_currency the currency code we want to get the exchange rate for.
                  Returns
                  -------
             GetForeignExchangeRateResponse
        """
        endpoint = "paga-webservices/merchant-rest/secured/getForeignExchangeRate"
        data = {'baseCurrency': base_currency, 'foreignCurrency': foreign_currency}

        print data

        pattern = base_currency + foreign_currency + self.api_key

        print pattern

        hash = self.generateHash(pattern)
        print hash

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_reconciliation_report(self, period_start_date, period_end_date):

        """ Reconciliation Report

                Parameters
                ----------
                period_start_date : string
                    period_start_date The datetime period for the reconciliation report to start
                period_end_date : string
                    period_end_date The datetime period for the reconciliation report ends
                Returns
                 -------
           ReconciliationReportResponse
        """

        endpoint = "paga-webservices/merchant-rest/secured/reconciliationReport"

        data = {'periodStartDateTimeUTC': period_start_date, 'periodEndDateTimeUTC': period_end_date}

        pattern = period_end_date + period_start_date + self.api_key

        hash = self.generateHash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def refund_bill(self, reference_number, include_customer_fee, full_refund, refund_amount, currency_code,
                    reason, customer_phone_number):
        """Refund Payment
        :param reference_number: The unique reference number provided as part of the original transaction which
        identifies the transaction to be refunded.
        :param include_customer_fee:includesCustomerFee Indicates whether the refund includes the customer fee (true)
         or not (false)
        :param full_refund:Indicates whether the refund is full or partial
        :param refund_amount: Only provided for a partial refund, this indicates the amount to be refunded.
        :param currency_code: The currency used in the transaction.
        :param reason: Human readable reason for refund
        :param customer_phone_number: The phone number of the customer that performed the operation
        :return: RefundPaymentResponse
        """

        endpoint = "paga-webservices/merchant-rest/secured/refundBillPay"

        data = {'referenceNumber': reference_number,
                'includesCustomerFee': include_customer_fee,
                'fullRefund': full_refund,
                'refundAmount': refund_amount,
                'currencyCode': currency_code,
                'reason': reason,
                'customerPhoneNumber': customer_phone_number}

        pattern = reference_number + refund_amount + customer_phone_number + self.api_key

        hash = self.generateHash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def build_header(self, hash_strings):
        headers = {
            'credentials': self.credential,
            'Accept': 'application/json',
            'principal': self.principal,
            'hash': hash_strings,
            'Content-Type': 'application/json'
        }
        return headers

    def url(self, test):
        if test:
            return test_server
        else:
            return live_Server

    def generateHash(self, pattern):
        hash = hashlib.sha512()
        hash.update(('%s' % (pattern)).encode('utf-8'))
        generated_hash = hash.hexdigest()
        return generated_hash
