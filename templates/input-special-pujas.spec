*** Model: SpecialPuja ***

*** SelectData: special_pujas; special_puja_id, contacts; contact_id ***

** special_pujas **
special_puja_id
puja_date: i (date; Puja Date; )@*, #0(DateColumn; Puja Date)?^
occasion_id: $(occasion_id), i (select; Occasion; occasions)
sevak_name: i (text; Sevak Name), #2(DataColumn; Sevak Name)?^
relationship_id: $(relationship_id), i (select; Relationship; relationships),
active: i (checkbox; Active; true), #5(ActiveColumn; Active)

** occasions **
occasion_id
name as occasion_name: #1(DataColumn; Occasion)?^

** relationships **
relationship_id
name as relationship_name: #3(DataColumn; Relationship)?
