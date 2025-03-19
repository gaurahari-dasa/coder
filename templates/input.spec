*** Model: Guide ***

*** SelectData: guides; guide_id, contacts; contact_id ***

** guides **
guide_id
name: i (text; Name; )@*, # (; Name; )?^
email: i (email; Email), # (; Email; )?^
mobile: i (text; Mobile)*, # (; Mobile; )?^
photo_path: i (file; Photo), # (%ImageColumn; ; ~file)?^
# dob: i (date; DOB), # (~date-only)
active: i (checkbox; Active; false), # (ActiveColumn; Active; )
contact_id: $(contacts)
language_id: $(languages), i (select; Language; languages)

** languages **
language_id
name as language_name
