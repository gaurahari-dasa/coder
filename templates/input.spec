*** Model: Guide, Contact ***

*** SelectData: guides; guide_id, contacts; contact_id ***

** guides **
guide_id
name: i (text; Name; )@*, #1(DataColumn; Name; )?^
email: i (email; Email), #2(DataColumn; Email; )?^
mobile: i (text; Mobile)*, #3(DataColumn; Mobile; )?^
photo_path: i (file; Photo), #4(ImageColumn; ;)?^, ~(file)
dob: i (date; DOB), ~(date-only)
active: i (checkbox; Active; false), #6(ActiveColumn; Active; )
language_id: $(language_id), i (select; Language; languages)

** languages **
language_id
name as language_name

*** Routes ***
