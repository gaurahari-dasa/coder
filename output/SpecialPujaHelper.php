<?php

namespace App\Helpers;

use App\Models\SpecialPuja;
// use App\Models\Contact;
// use App\Traits\ContactContext;

class SpecialPujaHelper
{
    // use ContactContext;

    public static function listAll($sortField = null, $sortDir = null)
    {
        
            if ($sortField === 'id') {
                $sortField = 'special_puja_id';
            }
            
        return SpecialPuja
            ::orderBy($sortField ?? @@@ default_sort_field @@@, $sortDir ?? 'asc')
			// ->join('contacts', 'addresses.contact_id', '=', 'contacts.contact_id')
            // ->leftJoin('countries', 'addresses.country_id', '=', 'countries.country_id')
            ->select(
                'special_pujas.special_puja_id',
'special_pujas.puja_date',
'special_pujas.sevak_name',
'special_pujas.active',
'occasions.occasion_id',
'occasions.name as occasion_name',
'relationships.relationship_id',
'relationships.name as relationship_name',
            );
    }

    public static function paginate($contactId)
    {
        $rowCount = request('row-count') ?? 5;
        $searchKey = request('search-key');
        $sortField = request('sort-field');
        $sortDir = request('sort');
        $items = self::listAll(Utils::snakeCase($sortField), $sortDir)
->where('special_pujas.contact_id', $contactId);

        if ($searchKey) {
            $items = $items->whereAny([
                'special_pujas.puja_date',
'special_pujas.sevak_name',
'occasions.name',
'relationships.name',
            ], 'like', "%{$searchKey}%");
        }

        return $items->paginate($rowCount)
            ->through(function ($item) {
                return [
                    'id' => $item->special_puja_id,
'pujaDate' => $item->puja_date,
'sevakName' => $item->sevak_name,
'active' => $item->active,
'occasionId' => $item->occasion_id,
'occasionName' => $item->occasion_name,
'relationshipId' => $item->relationship_id,
'relationshipName' => $item->relationship_name,
                ];
            })
            ->appends(['row-count' => $rowCount])
            ->appends(['search-key' => $searchKey])
            ->appends(['sort-field' => $sortField])
            ->appends(['sort' => $sortDir]);
    }

    public static function addEntity($validated)
    {
        return LogActivityHelper::create(function () use ($validated) {
            return SpecialPuja::create([
'puja_date' => Utils::parseDate($validated['pujaDate']),
'occasion_id' => $validated['occasionId'],
'sevak_name' => $validated['sevakName'],
'relationship_id' => $validated['relationshipId'],
'active' => $validated['active'],
'contact_id' => request('contactId'),
]);
        });
    }

    public static function updateEntity(SpecialPuja $specialPuja, array $validated)
    {
        $specialPuja->puja_date = Utils::parseDate($validated['pujaDate']);
$specialPuja->occasion_id = $validated['occasionId'];
$specialPuja->sevak_name = $validated['sevakName'];
$specialPuja->relationship_id = $validated['relationshipId'];
$specialPuja->active = $validated['active'];
LogActivityHelper::save($specialPuja);
return $specialPuja;
    }
}
