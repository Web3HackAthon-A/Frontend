from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3
from web3 import Account
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware
import json
import ipfshttpclient
import os
import environ
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_ABI_PATH = os.path.join(BASE_DIR, 'myapp', 'token_abi.json')
NFT_ABI_PATH = os.path.join(BASE_DIR, 'myapp', 'nft_abi.json')

#アドレスは一旦はハードコーディング
TOKEN_CONTRACT_ADDRESS = '0x014AB673309fC40E87A969Ae1Be334c0dd84dEb6'

with open(TOKEN_ABI_PATH) as f:
    TOKEN_ABI = json.load(f)

NFT_CONTRACT_ADDRESS = '0xe4a693a844641c5f0d4210c83cb87d197698a5e7'

with open(NFT_ABI_PATH) as f:
    NFT_ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/e0f9f3150fec48b7922a2c81553ad952'))

connection_check = w3.is_connected()
print(connection_check)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

private_key = env('PRIVATE_KEY')

assert private_key is not None, "You must set PRIVATE_KEY environment variable"
# assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

print(f"Your hot wallet address is {account.address}")

#ファイルアップロード後画面
# def upload_index(request):
#     return render(request, 'upload.html')

#初期画面
@csrf_exempt
def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'upload':
            return upload(request)
        elif action == 'view_content':
            return view_content(request)
    
    return render(request, 'index.html')

#コンテンツを観覧する場合のトークン発行
@csrf_exempt
def view_content(request):
    user = request.user
    content_id = request.POST.get('content_id')
    # token_name = request.POST.get('name')
    # token_symbol = request.POST.get('symbol')
    # token_decimals = 18
    # token_total_supply = request.POST.get('totalSupply')

    contract = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_CONTRACT_ADDRESS), abi=TOKEN_ABI)

    tx_hash = contract.functions.transfer(user, 1).transact()

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if tx_receipt['status'] == 1:
        return HttpResponse("Token creation successful")
    else:
        return HttpResponse("Token creation failed")

#ファイルのIPFSアップロード
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        file_data = uploaded_file
        # file_path = uploaded_file.temporary_file_path()

        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        res = client.add(file_data)
        request.session['ipfs_hash'] = res['Hash']
        return redirect('confirm')
    else:
        return HttpResponse('Method not allowed')

#IPFSアップロード確認ページ
def confirm(request):
    return render(request, 'confirm.html', {'ipfs_hash': request.session['ipfs_hash']})

#コンテンツを載せた場合のNFTとトークン発行
@csrf_exempt
def create_nft(request):
    if request.method == 'POST':
        user = '0xEAf7b8e119499b4ed318845dd4E0593f7Bb9607F'
        # uploaded_file = request.FILES['document']

        # client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        # res = client.add(uploaded_file)
        ipfs_hash = request.session.get('ipfs_hash')
        # token_id = request.POST.get('token_id')

        if not ipfs_hash:
            return HttpResponse('No file uploaded')

        # token_id = int(token_id)

        ipfs_url = f"https://ipfs.io/ipfs/{ipfs_hash}"

        balance = w3.eth.get_balance(Web3.to_checksum_address(user))


        # Reference the deployed contract:
        # billboard = w3.eth.contract(address=deployed_addr, abi=abi)

        contract = w3.eth.contract(address=Web3.to_checksum_address(user), abi=NFT_ABI)

        # tx_hash = contract.constructor("gm").transact({"from": acct2.address})
        # receipt = w3.eth.get_transaction_receipt(tx_hash)
        # deployed_addr = receipt[NFT_CONTRACT_ADDRESS]

        built_tx = contract.functions.mintNFT(ipfs_url).build_transaction({
            "nonce": w3.eth.get_transaction_count(account.address)
        })
        
        signed_tx = w3.eth.account.sign_transaction(built_tx, private_key=account.key)

        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return render(request, 'transaction_receipt.html', {'tx_receipt': tx_receipt})

    # if tx_receipt['status'] == True:
    #     tx_hash = contract.functions.transfer(user, 1).transact()
    #     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    #     if tx_receipt['status'] == True:
    #         return render(request, 'transaction_receipt.html', {'tx_receipt': tx_receipt})
    #         # return HttpResponse("NFT creation successful")
    #     else:
    #         return HttpResponse("Token granting failed")
    # else:
    #     return HttpResponse("NFT creation failed")
    