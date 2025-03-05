*** Model: Guide ***
'name',
'email',
'mobile',
'whatsapp',
'photo_path',
'active',

PK: address_id


*** SelectData: contacts, contact_id ***

** guides **
guide_id
name: #("Name" ?^), i(text|Name|@*)
email: #("Email" ?^), i(email|Email)
mobile: #("Mobile" ?^), i(text|Mobile)
whatsapp: #("Whatsapp" ?^), i(text|Whatsapp)
photo_path: ~(file), #(ImageColumn ?^), i(file|Photo)
active: #("Active" ActiveColumn), i(checkbox|Active)
