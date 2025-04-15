*** Model: ContactRelationship ***

*** SelectData: contact_relationships; contact_relationship_id, contacts; contact_id ***

** contact_relationships **
relation_pair_id: $(relation_pair_id), i (select; Relationship; relationships)@*
source_contact_id: $(source_contact_id), i (text; Relative Name; )*
active: i (checkbox; Active; true), #5(ActiveColumn; Active)

** contacts **
contact_id as source_contact_id
photo_path as source_contact_photo: #2(ImageColumn;), ~(file)
name as source_contact_name: #3(DataColumn; Name)?^
gender as source_contact_gender
mobile as source_contact_mobile: #4(DataColumn; Mobile)?^
whatsapp as source_contact_whatsapp

** relation_pairs **
relation_pair_id
name as relation_pair_name: #1(DataColumn; Name; )?^
