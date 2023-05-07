## Story:  
- As a developer, I want to implement role based access control for streamlit dashboards
## Assumptions  
- User Authentication is done by authentication module  - out of scope  
- Dashboard module needs to get  User, Role Group details using Authentication module/API   
- Dashboard module will store the user and role group information in cache/session - In scope  
- Dashboard module will check permission to see whether user has access   