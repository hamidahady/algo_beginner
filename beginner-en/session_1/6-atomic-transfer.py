# 1. add imports
# 2. copy/paste code from previous example above the break
# 3. add new code below the break
from pprint import pprint
import algokit_utils as algokit
import algosdk

def main():
     # use new_account() method to generate a new account
    my_account = algokit.Account.new_account()
    # print the address of the account object
    print("address: ",my_account.address)

    # instatiate algod client on localnet by running this in the command prompt: clear
    
    algod = algokit.get_algod_client(algokit.get_default_localnet_config("algod"))

    # instatiate kmd client on localnet, KMD: key management daemon, it is a wallet that holds all the accounts that we are going to have
    kmd = algokit.get_kmd_client_from_algod_client(algod)

    # fund my_account with ALGO from localnet dispenser 
    # min_spending_balance_micro_algos: how many algo this account want to have at the end of the transaction, 
    # 1_000_000 is 1 algo with percision of 6
    # to have an account in algo BC you need a minimum balance which is 0.1 algo to represent an account 0.1 algo is 1_00_000
    algokit.ensure_funded(
        algod,
        algokit.EnsureBalanceParameters(
            account_to_fund= my_account,
            min_spending_balance_micro_algos=  1_000_000 
        ))

    # create an ASA (Algorand Standard Asset, token, asset, NFT, etc.) , for creating an asset the minimum algo is 0.2 and for crfeating an account we have to have 0.1 algo
    unsigned_txn = algosdk.transaction.AssetCreateTxn(
        sender = my_account.address,
        sp = algod.suggested_params(), # suggested parameters
        total = 1,         # for NFT
        decimals = 0,   # for NFT
        default_frozen = False)
    
    # sign transaction
    signed_txn = unsigned_txn.sign(my_account.private_key)

    # submit transaction
    txid = algod.send_transaction(signed_txn)
    print("sent transaction ASA in txn: ",txid)
 
    # again, get info about my_account from algod
    pprint(algod.account_info(my_account.address))

    # print the assetID of my new asset from algod
    results = algod.pending_transaction_info(txid)
    assetID = results["asset-index"]
    print("assetID: ", assetID)

    # create other_account
    other_account = algokit.Account.new_account()

    # fund other_account with ALGO from localnet dispenser
    algokit.ensure_funded(
        algod,
        algokit.EnsureBalanceParameters(
            account_to_fund= other_account,
            min_spending_balance_micro_algos= 1_000_000 
        ))

    # OPTIN to ASA for other_account, holding an asset on top of the account increase our minimum balance requirement
    # we must tell network to want to hold an asset from an account 
    # asset_transfer_txn amount = 0 index=ASA to= self
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender = other_account.address,
        sp = algod.suggested_params(), # suggested parameters
        receiver = other_account.address,
        amt = 0,
        index = assetID)

    # sign transaction
    signed_txn = unsigned_txn.sign(other_account.private_key)
    # submit transaction
    txid = algod.send_transaction(signed_txn)
    print("OPTIN ASA in txn: ",txid)

    # view other_account to confirm assest transfer
    print(algod.account_info(other_account.address))
    
    # send asset from my_account to other_account
    unsigned_txn = algosdk.transaction.AssetTransferTxn(
        sender = my_account.address,
        sp = algod.suggested_params(), # suggested parameters
        receiver = other_account.address,
        amt = 1,
        index = assetID)
        
    # sign transaction
    signed_txn = unsigned_txn.sign(my_account.private_key)
    # submit transaction
    txid = algod.send_transaction(signed_txn)
    print("sent ASA in txn: ",txid)
    # view other_account to confirm assest transfer,it should have 01 amount after transfer
    print(algod.account_info(other_account.address))
    # view other_account to confirm assest transfer, it should have 0 amount after transfer
    print(algod.account_info(my_account.address))

    #####################################################################
    # NEW BELOW
    #####################################################################

    # 1. Create multiple transactions
    # 2. Group them (order is important)
    # 3. Sign the individual transactions within the group
    # 4. Send the signed transaction group
    # txn_1 is Payment 1 ALGO from other_account to my_account
    # txn_2 is AssetTransfer of 1 indexID from my_account to other_account
    # groupTxn = [txn1, txn2]
    # both will complete atomiclly, else none will be confirmed
    
    # send 1 ALGO from other_account to my_account
    payment_txn = algosdk.transaction.PaymentTxn(
        sender = other_account.address,
        sp = algod.suggested_params(),
        receiver = my_account.address,
        amt = 1_000_000
    )
    # send asset from my_account to other_account (this was unsigned transaction in previous sections)
    asset_xfer_txn = algosdk.transaction.AssetTransferTxn(
        sender=my_account.address,
        sp= algod.suggested_params(),
        receiver= other_account.address,
        amt=1,
        index= assetID
    )
    # group transactions
    group_id = algosdk.transaction.calculate_group_id([payment_txn,asset_xfer_txn])
    payment_txn.group = group_id
    asset_xfer_txn.group = group_id
    # sign transactions
    stxn1 = payment_txn.sign(other_account.private_key)
    stxn2 = asset_xfer_txn.sign(my_account.private_key)
    # assemble transaction group
    signed_group = [stxn1,stxn2]

    #submit atomic transaction group
    txid = algod.send_transactions(signed_group)
    print("sent atomic transfer: ", txid)

    # view accounts to confirm atomic transfer
    pprint(algod.account_asset_info(my_account.address))
    pprint(algod.account_asset_info(other_account.address))
main()
