*** Model: Guide ***

*** SelectData: guides; guide_id ***

** guides **
guide_id
name: i (text; Name; )@*, # (; Name; )?^
email: i (email; Email), # (; Email; )?^
mobile: i (text; Mobile)*, # (; Mobile; )?^
photo_path: i (file; Photo), # (%ImageColumn; ; ~file)?^
dob: i (date; DOB), # (~date-only)
active: i (checkbox; Active), # (ActiveColumn; Active; )
contact_id: $()

** languages **
language_id: i (select; Language; languages)
name as language_name
