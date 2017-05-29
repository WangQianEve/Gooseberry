# Data
## Session
+ uid
+ uname

## User
+ uid
+ uname
+ timetable
+ contacts
  + id
  + nickname
+ invitationS
+ invitationJ
+ timezone
## Invitation
+ inv_id
+ main_slot
  [inv_slot]: start_time, end_time, support(list of id,name,image), against(list of id,name,image)
+ alt_slot
  list of inv_slot
+ status
  + voting
  + finished
    final_slot
