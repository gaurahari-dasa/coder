*** Model: Guide ***
name
email
mobile
photo_path
dob
active

*** SelectData: guides; guide_id ***

** guides **
guide_id
name: # (; Name; )?^, i (text; Name; )@*
email: # (; Email; )?^, i (email; Email)
mobile: # (; Mobile; )?^, i (text; Mobile)*
photo_path: # (%ImageColumn; ; ~file)?^, i (file; Photo)
dob: # (~date-only), i (date; DOB)
active: # (ActiveColumn; Active; ), i (checkbox; Active)
contact_id: $()

** languages **
language_id: i (select; Language; languages)
name as language_name
