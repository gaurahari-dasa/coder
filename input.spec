*** Model: EventTemplate ***

*** Routes: /event-template(event_templates) ***

*** SelectData: event_templates; event_template_id ***

** event_templates **
event_template_id
event_type: i(select; Event Type; eventTypes; )*, #0(DataColumn; Event Type)
name: i(text; Name; 500; )*, #1(DataColumn; Event Name)?^1
url: i(text; URL; 2000; )
location: i(text; Location; 2000; )
description: i(text; Description; 2000; )
genders: i(select; Target Gender; genders; )
guide_id: $(guide_id), i(select; KL Guide; guides; guideName)
community_id: $(community_id), i(select; Community; communities; communityName)
event_category_id: $(event_category_id), i(select; Category; eventCategories; eventCategoryName)
image_path: i(file; Image; ; ), #2(ImageColumn; Image)
regend_datetime: i(datetime-local; Registration Deadline; ; )
grace_time: i(text; Grace Time; 4; )
with_prasadam: i(checkbox; Prasadam; true; ), #3(ActiveColumn; Prasadam)
event_price: i(text; Event Price; 10; )*, #4(CurrencyColumn; Event Price)^2
prasadam_price: i(text; Prasadam Price; 10; )*, #5(CurrencyColumn; Prasadam Price)^3
discountable: i(checkbox; Discountable; true; ), #6(ActiveColumn; Discountable)
capacity: i(text; Slots; 8; )
frequency: i(select; Frequency; frequency; )*, #7(DataColumn; Frequency)
dayspec: i(select; Weekday; weekdays; )
start_date: i(date; Start Date; ; )*, #8(DateColumn; Start Date)
start_time: i(date; Start Time; ; )*, #9(DataColumn; Start Time)
end_date: i(date; End Date; ; )
end_time: i(date; End Time; ; )
active: i(checkbox; Active; false; ), #10(ActiveColumn; Active)

** communities **
community_id
name as community_name
location as community_location

** event_categories **
event_category_id
name as event_category_name: #11(DataColumn; Category)

** guides **
guide_id
name as guide_name
code_name as guide_code_name
