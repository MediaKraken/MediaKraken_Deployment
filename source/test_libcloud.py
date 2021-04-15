from libcloud.storage.providers import DRIVERS

print(DRIVERS)
for storage_provider in DRIVERS:
    print(storage_provider, DRIVERS[storage_provider])

