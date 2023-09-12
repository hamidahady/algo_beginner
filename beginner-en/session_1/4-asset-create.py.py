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

    # instatiate algod client on localnet by running this in the command prompt:  algokit localnet start
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
        )
    )

    #####################################################################
    # NEW BELOW
    #####################################################################

    # create an ASA (Algorand Standard Asset, token, asset, NFT, etc.) , for creating an asset the minimum algo is 0.2 and for crfeating an account we have to have 0.1 algo
    unsigned_txn = algosdk.transaction.AssetCreateTxn(
        sender = my_account.address,
        sp = algod.suggested_params(), # suggested parameters
        total = 1,         # for NFT
        decimals = 0,   # for NFT
        # considering total & decimals in above, total= 100 & decimals =2 are equivalent
        default_frozen = False # means we want to be bale to transfer the asset
    )
    
    # sign transaction
    signed_txn = unsigned_txn.sign(my_account.private_key)

    # submit/send transaction to the network
    txid = algod.send_transaction(signed_txn)
    print("222222222222222222222222222222222222222222")
    print("created transaction ASA in txn: ",txid)
 
    # again, get info about my_account from algod
    print("333333333333333333333333333333333333333333")
    pprint(algod.account_info(my_account.address))

    # print the assetID of my new asset from algod, the transaction is submitted not approved yet. So it is pending!
    results = algod.pending_transaction_info(txid)
    print("444444444444444444444444444444444444444444")
    print(results)
    assetID = results["asset-index"]
    print("555555555555555555555555555555555555555555")
    print("assetID: ", assetID)
main()

