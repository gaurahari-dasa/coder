*** Model: User ***



*** Routes: /users(users) ***
#index: visit_guides
#store: add_guides
#update: edit_guides



*** SelectData: users; id ***

** users **
id
name as user_name: i (text; Name; 255)@*, #1(DataColumn; Name; )?^0
email: i (email; Email; 255)*, #2(DataColumn; Email; )?^
mobile: i (text; Mobile; 10), #3(DataColumn; Mobile; )?^
active: i (checkbox; Active; false), #4(ActiveColumn; Active; )
