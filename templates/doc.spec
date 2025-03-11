*** Model: Guide ***
'name',
'email',
'mobile',
'whatsapp',
'photo_path',
'active',

PK: address_id


*** SelectData: contacts, contact_id ***

** contacts **
contact_id
name: t("Name" ?^)
email: t("Email" ?^)
mobile: t("Mobile" ?^)
whatsapp: t("Whatsapp" ?^)
photo_path: t(/file/ "" <ImageColumn> ?^), i(Photo|file)
active: t("Active" <ActiveColumn>)

** professions **
profession_id
name as profession_name

** sources **
source_id
name as source_name

** categories **
category_id
name as category_name

** contact_statuses **
contact_status_id
name as contact_status_name

** guides **
guide_id
name as guide_name


*** UI ***
    line1: text, Address Line 1
    line2: text, Address Line 2
    area: text, Area
    city: text, City
    state: select, State, states
    country: select, Country, countries
    mailing: checkbox, Mailing
    addressType: select, Type
	pin_code: text, PIN Code
    active: checkbox, Active
	guide: select, Guide, guides
******