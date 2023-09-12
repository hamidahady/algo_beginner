# 1. add imports
# 2. copy/paste code from previous example above the break
# 3. add new code below the break

from pprint import pprint
import algokit_utils as algokit

def main():
    # use new_account() method to generate a new account
    my_account = algokit.Account.new_account()
    # print the address of the account object
    print("address: ",my_account.address)

    #####################################################################
    # NEW BELOW
    #####################################################################
    
    #****** if you are using your local machine in terminal of linux do this: sudo service docker start
    # check the the status of docker engine with: "docker ps" if you received "permission denied " do the below:
    # "sudo chmod 666 /var/run/docker.sock"
    # then: instatiate algod client on localnet by running this in the command prompt:  algokit localnet start
    algod = algokit.get_algod_client(algokit.get_default_localnet_config("algod"))
    # algokit provides a client to communicate with blockchain

    # print the version for algod
    print("algod is running version ",algod.versions())
    print("###########################################")
    # from the blockchain, get info about my_account from algod
    pprint(algod.account_info(my_account.address))
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
    print("========================================")
    # for holding an account we need to have 0.1 algo, since the balance should be 1 algo available, the total amount is raised to 1.1 algo
    # again, get info about my_account from algod
    pprint(algod.account_info(my_account.address))
main()