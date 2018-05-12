import argparse
import requests

blockchain_url  = "https://blockchain.info/"

parser = argparse.ArgumentParser(description='Collect stats on Bitcoin transactions and any related hidden services.')

parser.add_argument("--address", help="A bitcoin address to begin the search on.",)

args = parser.parse_args()

bitcoin_address = args.address

def get_transaction_counts(bitcoin_address):

    address_response = requests.get(blockchain_url + 'rawaddr/' + bitcoin_address)

    address_details = address_response.json()

    total_tx = address_details['n_tx']
    print("Number of total transactions %d" % total_tx)

    # total_tx =
    # print("Number of received transactions  %d", % total_tx)
    #
    # total_tx =
    # print("Number of sent transactions %d", % total_tx)

# def get_transaction_timeline(bitcoin_address):


print("* Retrieving all transactions from the blockchain for %s" % bitcoin_address)

print("* Stats on transaction counts")

get_transaction_counts(bitcoin_address)
