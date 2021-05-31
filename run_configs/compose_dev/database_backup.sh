docker exec -t mkstack_database pg_dump -U postgres > mkstack_database_dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql
#docker exec -t mkstack_database pg_dumpall -c -U postgres > mkstack_database_dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql
#docker exec -t mkstack_database pg_dump -c -U postgres -Fc postgres > mkstack_database_dump_`date +%Y-%m-%d"_"%H_%M_%S`.dump