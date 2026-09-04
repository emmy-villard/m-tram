# DataBase Table Schemas
This document provides a complete list of the database table schemas.

The schema updates are tracked with alchemy. Since the test_database keeps the same structure as the app database, we use the test database to track migrations.

## Dynamic MData
### trr
- trr_id : TEXT
- trr_time : TIMESTAMP
- trr_nsv_id : INT between 1 and 4 included
- Primary key : trr_id, trr_time

### ligne
- ligne_id : TEXT
- ligne_time : TIMESTAMP
- ligne_nsv_id : INT between 1 and 4 included
- Primary key : ligne_id, ligne_time