*** Model: Contact ***

*** SelectData: contacts; contact_id ***

** contacts **

salutation_id: $(salutation_id), i (select; Salutation; salutations)
mother_tongue: $(mother_lang_id), i (select; Mother Tongue; languages)
marital_status: i (select; Marital Status; marital_statuses), #()^
company_name: i (text; Company Name), #()?^
linked_in: i (text; LinkedIn), #()?^
designation: i (text; Designation), #()?^
birth_state: $(state_id), i (auto; Birth State; states)


** languages **
language_id as mother_lang_id
name as mother_lang_name: #()?

** salutations **
salutation_id
name as salutation_name

** states **
state_id
name as state_name: #()?^