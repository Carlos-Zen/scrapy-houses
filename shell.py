# -*- coding: utf-8 -*-
from shells import mongo

# mongo.delete_dups_row('house', 'house_shanghai')
# mongo.test_insert_dups('house', 'house_shanghai')

# mongo.update_collections_posotion()
# mongo.delete_collections_dups_keys()

def main():
    mongo.update_collections_uniqe_keys()
if __name__ == "__main__":
    main()
# from bson.json_util import dumps