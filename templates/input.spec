*** Model: Guide, Contact ***



*** Routes: /guides(guides), /contacts(contacts) ***
#index: visit_guides
#store: add_guides
#update: edit_guides



*** SelectData: guides; guide_id, contacts; contact_id ***

** guides **
guide_id
name: i (text; Name; )@*, #1(DataColumn; Name; )?^0
email: i (email; Email), #2(DataColumn; Email; )?^
mobile: i (text; Mobile)*, #3(DataColumn; Mobile; )?^
photo_path: i (file; Photo), #4(ImageColumn; ;)?^, ~(file)
dob: i (date; DOB), ~(date-only)
active: i (checkbox; Active; false), #6(ActiveColumn; Active; )
language_id: $(language_id), i (select; Language; languages; languageName)

** languages **
language_id
name as language_name
