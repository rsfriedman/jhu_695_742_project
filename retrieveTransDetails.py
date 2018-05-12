import argparse
import requests
import json

block_explorer_url  = "https://blockexplorer.com/api/addr/"

parser = argparse.ArgumentParser(description='Collect info about bitcoin transactions.')

parser.add_argument("--address", help="A bitcoin address to begin the search on.",)

args = parser.parse_args()

bitcoin_address = args.address

def get_all_transactions(bitcoin_address):
    transactions = []
    block_explorer_url_full = block_explorer_url + bitcoin_address

    response = requests.get(block_explorer_url_full)
    results  = response.json()

    if results['txApperances'] == 0:
        print("**** No transactions found for %s" % bitcoin_address)
        return transactions


    transactions.extend(results['transactions'])
    bitcoin_addresses = {}

    for transaction in transactions:
        transaction_response = requests.get('https://blockexplorer.com/api/tx/' + transaction)
        if(transaction_response):
            transaction_result = transaction_response.json()
            addr = transaction_result['vin'][0]['addr']

            if addr in bitcoin_addresses:
                bitcoin_addresses[addr] += 1
            else:
                bitcoin_addresses[addr] = 1

            #walk through all recipients and check each address
            # for receiving_side in transaction_result['vout']:
            #
            #     if "addresses" in receiving_side['scriptPubKey']:
            #
            #         for address in receiving_side['scriptPubKey']['addresses']:
            #             if address in bitcoin_addresses:
            #                 bitcoin_addresses[address] += 1
            #             else:
            #                 bitcoin_addresses[address] = 1

    print("%d unique bitcoin addresses found" % len(bitcoin_addresses))
    return bitcoin_addresses

def parse_transaction_count(transaction_count):
    parsed_tx_count = {}
    for key, value in transaction_count.items():
        if(value>2):
            parsed_tx_count[key] = value
    return parsed_tx_count

print("*** Retrieving all transactions for %s" % bitcoin_address)

transaction_count = get_all_transactions(bitcoin_address)

parsed_count = parse_transaction_count(transaction_count)

print("Finished count, writing to file, %d addresses with over 10 transactions found" % len(parsed_count))

file = open("tx_count.txt", "w")
file.write(json.dumps(parsed_count))
file.close()
