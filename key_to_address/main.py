from eth_account import Account
from web3 import Web3, exceptions

Account.enable_unaudited_hdwallet_features()

infura_api_key = 'api_key'

web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_api_key}'))

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

try:
    with open('mnemonics.txt', 'r') as file, open('wallets.txt', 'a') as output_file:
        for line in file:
            mnemonic = line.strip()

            if not mnemonic:
                continue

            try:
                private_key = Account.from_mnemonic(mnemonic)._private_key.hex()

                account = Account.from_key(private_key)
                address = account.address

                balance_wei = web3.eth.get_balance(address)
                balance_eth = balance_wei / 10**18 

                print(GREEN + "Ethereum Address:", address)
                print("Balance:", balance_eth, "ETH" + RESET)

                output_file.write(f"Ethereum Address: {address}\n")
                output_file.write(f"Balance: {balance_eth} ETH\n")
                output_file.write(f"Mnemonic: {mnemonic}\n")
                output_file.write(f"Private Key: {private_key}\n\n")

                if balance_eth > 0:
                    print("Found an Ethereum address with balance above 0. Stopping the program.")
                    break

            except exceptions.ValidationError:
                print(RED + f"Invalid private key for mnemonic" + RESET)

except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("An error occurred:", e)
