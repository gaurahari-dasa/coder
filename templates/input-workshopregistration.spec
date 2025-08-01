*** Model: WorkshopRegistration, Contact ***



*** Routes: /workshop-registrations(workshop_registrations), /contacts(contacts) ***
#index: visit_guides
#store: add_guides
#update: edit_guides



*** SelectData: workshop_registrations; id, contacts; contact_id ***

** workshop_registrations **
id
workshop_id: $ (workshop_id), i (select; Event; workshops; workshopName)*@
payment_mode: i (select; Payment Mode; paymentModes; paymentMode)*, #7(DataColumn; Mode)
ins_amount: i (text; Ins Amount; 18)*, #2(CurrencyColumn; Ins Amount; )
transaction_date: i (datetime-local; Transaction Date)
order_id: i (text; Order ID; 255)
ins_number: i (text; Ins Number; 255), #3(DataColumn; Ins Number; )?^
ins_date: i (date; Ins Date), #4(DateColumn; Ins Date; ), ~(date-only)
ins_bank: i (text; Ins Bank; 100), #5(DataColumn; Ins Bank; )?^
payment_status: #6(DataColumn; Status)
settlement_date: i (date; Settlement Date)
settlement_amount: i (text; Settlement Amount; 18)
source_id: $ (source_id), i (select; Source; sources; sourceName)*

** sources **
source_id
name as source_name: lookup

** workshops **
id as workshop_id
name as workshop_name: #1(DataColumn; Event)?^
