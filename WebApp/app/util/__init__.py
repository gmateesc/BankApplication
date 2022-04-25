from persistence import load_store



def seq_number():
    seq_number.counter += 1
    return seq_number.counter

seq_number.counter = 0



#
# Check that the JSON payload observes the schema
#
def request_check(account):

    import six

    str_type = six.string_types
    int_type = six.integer_types

    #
    # Check the types of the values of the top level keys
    #
    
    if (not isinstance(account['iban'],        str_type)) or  \
       (not isinstance(account['type'],        str_type)) or  \
       (not isinstance(account['currency'],    str_type)) or  \
       (not isinstance(account['customer_id'], int_type)):
        raise TypeError("invalid 'iban', 'type', 'currency' or 'customer_id' field")


    # Check IBAN = CHXX XXXX XXXX XXXX XXXX X
    if not account['iban'].startswith("CH"):
        raise TypeError("invalid 'IBAN', must start with 'CH'")

    # Check type
    if account['type'] not in ['checking', 'savings', 'foreign currency']:
        raise TypeError("invalid 'type', must be 'checking', 'savings', or 'foreign currency'")
    
    # Check currency
    if account['currency'] != '' and account['currency'] not in ['USD', 'EUR', 'GBP']:
        raise TypeError("invalid 'currency', must be 'USD', 'EUR', or 'GBP'")        


    # Generate new account ID
    account['id'] = str(seq_number())


#
# Save a new account: persist the account to a file
# and add it to the cache
#
def save_account(config, accounts, account ):

    # If the account is in cache, remove it from cache
    id = account['id']    
    old_account = list(filter( lambda e: e['id']==id, accounts ))
    if len(old_account) != 0:
        old = old_account[0]
        accounts.remove(old)

    # Add new account to cache
    accounts.append(account)

    # Persist account to DOCUMENT_ROOT
    file_name = config['DOCUMENT_ROOT'] + "/" + id + ".json"
    load_store.store_file(file_name, account)




#
# Load an account: 
#
def load_account(config, accounts, account_id ):

    #
    # If the account is in cache, get it from cache
    #

    cache_account = list( filter(lambda e: e['id']==account_id, accounts) )
    if len(cache_account) != 0:

        print("DEBUG: get account %s from cache " % (account_id) )
        account = cache_account
        
    else:

      #
      # Load account from file and add to cache
      #
      import os.path
      file_name = config['DOCUMENT_ROOT'] + "/" + str(account_id) + ".json"
      if os.path.isfile(file_name):
        print("DEBUG: get account %s from file " % (account_id) )
        account = [load_store.load_file(file_name) ]
      else:
        account = []

      # Add account to cache
      if len(account) != 0:
        accounts.append(account[0])

    if len(account) != 0:
        print("DEBUG: account is %s " % account[0] )

    return account

