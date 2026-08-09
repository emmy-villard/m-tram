# DataBase Table Schemas
This document provides a complete list of the database table schemas.

## Dynamic MData
### trr
- trr_id : TEXT
- trr_time : TIMESTAMP
- trr_nsv_id : INT
- Primary key : trr_id, trr_time

### new_trr_data (staging table)
- trr_id : TEXT
- trr_time : TIMESTAMP
- trr_nsv_id : INT
- Primary key : trr_id, trr_time

### ligne
- ligne_id : TEXT
- ligne_time : TIMESTAMP
- ligne_nsv_id : INT
- Primary key : ligne_id, ligne_time

### new_ligne_data (staging table)
- ligne_id : TEXT
- ligne_time : TIMESTAMP
- ligne_nsv_id : INT
- Primary key : ligne_id, ligne_time