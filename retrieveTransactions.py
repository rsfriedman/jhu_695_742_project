import argparse
import requests
import networkx

block_explorer_url  = "https://blockexplorer.com/api/addr/"

parser = argparse.ArgumentParser(description='Collect and graph Bitcoin transactions and any related addresses.')

parser.add_argument("--graph",help="Output file of the graph file)
parser.add_argument("--address", help="A bitcoin address to begin the search on.",)


args = parser.parse_args()

bitcoin_address = args.address
graph_file      = args.graph

#
# Retrieve all bitcoin transactions for a Bitcoin address
#
def get_all_transactions(bitcoin_address):

    transactions = []
    from_number  = 0
    to_number    = 50

    block_explorer_url_full = block_explorer_url + bitcoin_address

    response = requests.get(block_explorer_url_full)

    try:
        results  = response.json()
    except:
        print("[!] Error retrieving bitcoin transactions. Please re-run this script.")
        return transactions

    if results['txAppearances'] == 0:
        print("*** No transactions for %s" % bitcoin_address)
        return transactions

    transactions.extend(results['transactions'])

    while len(transactions) < results['txAppearances']:

        from_number += 50
        to_number   += 50

        block_explorer_url_full = block_explorer_url + bitcoin_address

        response = requests.get(block_explorer_url_full)

        results  = response.json()

        transactions.extend(results['transactions'])

    print("**** Retrieved %d bitcoin transactions." % len(transactions))

    return transactions

#
# Simple function to return a list of all unique
# bitcoin addresses from a transaction list
#
def get_unique_bitcoin_addresses(transaction_list):

    bitcoin_addresses = []

    for transaction in transaction_list:

        transaction_response = requests.get('https://blockexplorer.com/api/tx/' + transaction)
        if(transaction_response):
            transaction_result = transaction_response.json()

            # check the sending address
            if transaction_result['vin'][0]['addr'] not in bitcoin_addresses:
                bitcoin_addresses.append(transaction_result['vin'][0]['addr'])

            # walk through all recipients and check each address
            for receiving_side in transaction_result['vout']:

                if "addresses" in receiving_side['scriptPubKey']:

                    for address in receiving_side['scriptPubKey']['addresses']:

                        if address not in bitcoin_addresses:

                            bitcoin_addresses.append(address)

    print("[*] Identified %d unique bitcoin addresses." % len(bitcoin_addresses))

    return bitcoin_addresses


#
# Graph all of the Bitcoin transactions
#
def build_graph(source_bitcoin_address,transaction_list):

    graph = networkx.DiGraph()

    # graph the transactions by address
    for transaction in transaction_list:
        transaction_response = requests.get('https://blockexplorer.com/api/tx/' + transaction)
        if(transaction_response):
            transaction_result = transaction_response.json()

            # check the sending address
            sender = transaction_result['vin'][0]['addr']

            if sender == source_bitcoin_address:
                graph.add_node(sender)
            else:
                graph.add_node(sender)


            # walk through all recipients and check each address
            for receiving_side in transaction_result['vout']:

                if "addresses" in receiving_side['scriptPubKey']:
                    for address in receiving_side['scriptPubKey']['addresses']:

                        if address == source_bitcoin_address:
                            graph.add_node(address)
                        else:
                            graph.add_node(address)

                        graph.add_edge(sender,address)


    # write out the graph
    networkx.write_gexf(graph,graph_file)

    return


# get all of the bitcoin transactions
print("[*] Retrieving all transactions from the blockchain for %s" % bitcoin_address)

transaction_list = get_all_transactions(bitcoin_address)

if len(transaction_list) > 0:

    # get all of the unique bitcoin addresses
    bitcoin_addresses = get_unique_bitcoin_addresses(transaction_list)

    # graph the bitcoin transactions
    build_graph(bitcoin_address,transaction_list)

    print("[*] Done! Open the graph file and happy hunting!")
