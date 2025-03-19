<?php

namespace App\Helpers;

use App\Models\Guide;
// use App\Models\Contact;
// use App\Traits\ContactContext;

class GuideHelper
{
    // use ContactContext;

    public static function listAll($sortField = null, $sortDir = null)
    {
        return Guide
            ::orderBy($sortField ?? 'area', $sortDir ?? 'asc')
			// ->join('contacts', 'addresses.contact_id', '=', 'contacts.contact_id')
            // ->leftJoin('countries', 'addresses.country_id', '=', 'countries.country_id')
            ->select(
                'guides.guide_id',
'guides.name',
'guides.email',
'guides.mobile',
'guides.photo_path',
'guides.active',
'languages.language_id',
'languages.name as language_name',
            );
    }

    public static function paginate($count)
    {
        $searchKey = request('search-key');
        $sortField = request('sort-field');
        $sortDir = request('sort');
        $items = self::listAll(Utils::snakeCase($sortField), $sortDir)
->where('guides.contact_id', request('contact-id'));

        if ($searchKey) {
            $items = $items->whereAny([
                'line1',
                'line2',
                'area',
                'city',
                'pin_code',
                'addresses.state',
                'countries.name',
            ], 'like', "%{$searchKey}%");
        }

        return $items->simplePaginate($count)
            ->through(function ($item) {
                return [
                    'id' => $item->address_id,
                    'line1' => $item->line1,
                    'line2' => $item->line2,
                    'area' => $item->area,
                    'city' => $item->city,
                    'state' => $item->state,
                    'countryId' => $item->country_id,
                    'countryName' => $item->country_name,
                    'mailing' => $item->mailing,
                    'addressType' => $item->address_type,
                    'pinCode' => $item->pin_code,
                    'active' => $item->active,
                ];
            })
            ->appends(['contact-id' => request('contact-id')])
            ->appends(['search-key' => $searchKey])
            ->appends(['sort-field' => $sortField])
            ->appends(['sort' => $sortDir]);
    }

    public static function addAddress($validated)
    {
        return LogActivityHelper::create(function () use ($validated) {
            return Address::create([
                'line1' => $validated['line1'],
                'line2' => $validated['line2'],
                'area' => $validated['area'],
                'city' => $validated['city'],
                'state' => $validated['state'],
                'country_id' => $validated['country'],
                'mailing' => $validated['mailing'],
                'address_type' => $validated['addressType'],
                'pin_code' => $validated['pinCode'],
                'active' => $validated['active'],
                'contact_id' => request('contact'),
            ]);
        });
    }

    public static function updateAddress($validated)
    {
        $address = Address::find(request('id'));
        $address->line1 = $validated['line1'];
        $address->line2 = $validated['line2'];
        $address->area = $validated['area'];
        $address->city = $validated['city'];
        $address->state = $validated['state'];
        $address->country_id = $validated['country'];
        $address->mailing = $validated['mailing'];
        $address->address_type = $validated['addressType'];
        $address->pin_code = $validated['pinCode'];
        $address->active = $validated['active'];
        $address->contact_id = request('contact');
        LogActivityHelper::save($address);

        return $address;
    }
}
