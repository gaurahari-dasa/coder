*** Model: ContactRelationship ***

*** SelectData: contact_relationships; contact_relationship_id, contacts; contact_id ***

** contact_relationships **
relationship_id: $(relationship_id), i (select; Relationship; relationships)@*
source_contact_id: $(source_contact_id), i (text; Relative Name; )*
active: i (checkbox; Active; true), #5(ActiveColumn; Active)

** contacts **
contact_id as source_contact_id
photo_path as source_contact_photo: #2(ImageColumn;), ~(file)
name as source_contact_name: #3(DataColumn; Name)?^
mobile as source_contact_mobile: #4(DataColumn; Mobile)?^

** relationships **
relationship_id
name as relationship_name: #1(DataColumn; Name; )?^
