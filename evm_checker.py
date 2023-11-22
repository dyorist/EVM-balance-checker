import requests
import argparse
from web3 import Web3
from decimal import Decimal


def read_wallets(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]
    

def get_coin_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin]["usd"]


def get_wallet_info(wallet_addresses, provider, network, coin_price, coin_name):
    print(f"Checking wallets balance and transactions quantity in {network} network")
    w3 = Web3(Web3.HTTPProvider(provider))
    total_coin = 0
    total_usd = 0
    for address in wallet_addresses:
        balance = w3.from_wei(w3.eth.get_balance(address), 'ether')
        usd_balance = balance * Decimal(str(coin_price))
        nonce = w3.eth.get_transaction_count(address)
        print(f"Wallet {address} has {nonce} txs in {network}. Balance: {balance} {coin_name} = {round(usd_balance, 2)}$")
        total_coin += balance
        total_usd += usd_balance
    print(f"Total balance for checked wallets - {total_coin} {coin_name} = {round(total_usd, 2)}$\n")


networks = {
    "ETH":{ "provider":  "https://rpc.ankr.com/eth", "coin_id": "ethereum", "coin_name": "ETH"},
    "BSC":{ "provider": "https://rpc.ankr.com/bsc", "coin_id": "binancecoin", "coin_name": "BNB"},
    "Arbitrum":{ "provider":  "https://rpc.ankr.com/arbitrum", "coin_id": "ethereum", "coin_name": "ETH"},
    "Optimism":{ "provider":  "https://rpc.ankr.com/optimism", "coin_id": "ethereum", "coin_name": "ETH"},
    "Polygon":{ "provider":  "https://rpc.ankr.com/polygon", "coin_id": "matic-network", "coin_name": "MATIC"},
    "ZkSyncEra":{ "provider":  "https://rpc.ankr.com/zksync_era", "coin_id": "ethereum", "coin_name": "ETH"},
    "Avalanche":{ "provider": "https://rpc.ankr.com/avalanche", "coin_id": "avalanche-2", "coin_name": "AVAX"},
    "Scroll":{ "provider": "https://rpc.ankr.com/scroll", "coin_id": "ethereum", "coin_name": "ETH"},
    "BASE":{ "provider": "https://rpc.ankr.com/base", "coin_id": "ethereum", "coin_name": "ETH"},
    "Zora":{ "provider": "https://rpc.zora.energy", "coin_id": "ethereum", "coin_name": "ETH"},
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check balance and transactions of wallets.")
    parser.add_argument("networks", nargs='*', default=list(networks.keys()), help="Networks to check (e.g., ETH BSC). If not provided, all networks are checked.")
    args = parser.parse_args()

    wallet_addresses = read_wallets("wallets.txt")

    for network in args.networks:
        if network in networks:
            network_info = networks[network]
            provider = network_info["provider"]
            coin_id = network_info["coin_id"]
            coin_name = network_info["coin_name"]
            coin_price = get_coin_price(coin_id)
            print(f"Current price for {coin_name} is {coin_price}$")

            get_wallet_info(wallet_addresses, provider, network, coin_price, coin_name)
        else:
            print(f"Network {network} not found.")