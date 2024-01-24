from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3
import json
import ipfshttpclient
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_ABI_PATH = os.path.join(BASE_DIR, 'myapp', 'token_abi.json')
NFT_ABI_PATH = os.path.join(BASE_DIR, 'myapp', 'nft_abi.json')

TOKEN_CONTRACT_ADDRESS = '0x014AB673309fC40E87A969Ae1Be334c0dd84dEb6'

with open(TOKEN_ABI_PATH) as f:
    TOKEN_ABI = json.load(f)

NFT_CONTRACT_ADDRESS = '0x9fef1a325f1587007a52609d09fef5915d9c64ac'

with open(NFT_ABI_PATH) as f:
    NFT_ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider('0xEAf7b8e119499b4ed318845dd4E0593f7Bb9607F'))

@csrf_exempt
def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'upload_content':
            return create_nft(request)
        elif action == 'view_content':
            return view_content(request)
    
    return render(request, 'index.html')

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
    
@csrf_exempt
def create_nft(request):
    user = request.user
    uploaded_file = request.FILES['document']

    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = client.add(uploaded_file)

    ipfs_url = f"https://ipfs.io/ipfs/{res['Hash']}"

    print(ipfs_url)

    contract = w3.eth.contract(address=Web3.to_checksum_address(NFT_CONTRACT_ADDRESS), abi=NFT_ABI)

    tx_hash = contract.functions.create(uploaded_file.name, ipfs_url).transact()

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if tx_receipt['status'] == 1:
        tx_hash = contract.functions.transfer(user, 1).transact()
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt['status'] == 1:
            return HttpResponse("NFT creation successful")
        else:
            return HttpResponse("Token granting failed")
    else:
        return HttpResponse("NFT creation failed")
    