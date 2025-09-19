call_tool list_recent {"db_name":"modq","collection_name":"crm_processed_records","limit":5}


call_tool find_many {"db_name":"modq","collection_name":"crm_processed_records","filter":{"Type":"AccountInsight"},"sort":[["UpdatedTimestamp",-1]],"limit":3}


call_tool find_one {"db_name":"modq","collection_name":"crm_processed_records","filter":{"_id":"6689fa01d4f3f9cbeaa0a123"}}


