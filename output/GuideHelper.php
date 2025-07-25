<?php

namespace App\Helpers;

use App\Models\Guide;
use App\Traits\ContactContext;

class GuideHelper
{
use ContactContext;

    public static function listAll(?string $sortField = null, ?string $sortDir = null)
    {
        if ($sortField === 'id') {
                $sortField = 'guide_id';
        }
            
        return Guide
            ::orderBy($sortField ?? 'guides.name', $sortDir ?? 'asc')
            ->join('languages', 'guides.language_id', '=', 'languages.language_id')
->select(
                'guides.guide_id',
'guides.name',
'guides.email',
'guides.mobile',
'guides.photo_path',
'guides.dob',
'guides.active',
'languages.language_id',
'languages.name as language_name',
            );
    }

    public static function paginate(int $contactId)
    {
        $rowCount = request('row-count') ?? 5;
        $searchKey = request('search-key');
        $sortField = request('sort-field');
        $sortDir = request('sort');
        $items = self::listAll(Utils::snakeCase($sortField), $sortDir)
->where('guides.contact_id', $contactId);

        if ($searchKey) {
            LogAccessHelper::log(Guide::class, $searchKey);
            $items = $items->whereAny([
                'guides.name',
'guides.email',
'guides.mobile',
'guides.photo_path',
            ], 'like', "%{$searchKey}%");
        }

        return $items->paginate($rowCount)
            ->through(function ($item) {
                return [
                    'id' => $item->guide_id,
'name' => $item->name,
'email' => $item->email,
'mobile' => $item->mobile,
'photoPath' => Utils::asset($item->photo_path),
'dob' => Utils::formatDateJs($item->dob, DateFormatJs::OnlyDate),
'active' => $item->active,
'languageId' => $item->language_id,
'languageName' => $item->language_name,
                ];
            })
            ->appends(['row-count' => $rowCount])
            ->appends(['search-key' => $searchKey])
            ->appends(['sort-field' => $sortField])
            ->appends(['sort' => $sortDir]);
    }

    public static function addEntity(array $validated)
    {
        return LogActivityHelper::create(function () use ($validated) {
            return Guide::create([
'name' => $validated['name'],
'email' => $validated['email'],
'mobile' => $validated['mobile'],
'photo_path' => $validated['photoPath'],
'dob' => Utils::parseDate($validated['dob']),
'active' => $validated['active'],
'language_id' => $validated['languageId'],
'contact_id' => request('contactId'),
]);
        });
    }

    public static function updateEntity(Guide $guide, array $validated)
    {
        $guide->name = $validated['name'];
$guide->email = $validated['email'];
$guide->mobile = $validated['mobile'];
$guide->photo_path = $validated['photoPath'];
$guide->dob = Utils::parseDate($validated['dob']);
$guide->active = $validated['active'];
$guide->language_id = $validated['languageId'];
LogActivityHelper::save($guide);
    }
}
