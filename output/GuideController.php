<?php

namespace App\Http\Controllers;

use App\Helpers\GuideHelper;
use App\Helpers\ListingHelper;
use App\Helpers\MenuHelper;
use App\Helpers\UserHelper;
use App\Models\Guide;
use App\Models\Contact;
use Illuminate\Http\Request;

class GuideController extends Controller
{
    public function index(int $contactId)
    {
        return inertia('Guides/Index', [
            'menus' => MenuHelper::list(),
            'privileges' => UserHelper::privileges(request()->user(), 'contacts'),
            'guides' => GuideHelper::paginate($contactId),
'contactId' => $contactId,
    'contact' => GuideHelper::contactDetails(),
'languages' => HelperClass::list()->get(),
            'searchKey' => request('search-key'),
            'sortField' => request('sort-field'),
            'sortDir' => request('sort'),
        ]);
    }

    public function store()
    {
        $validated = request()->validate([
            'name' => '',
'email' => '',
'mobile' => '',
'photoPath' => '',
'dob' => '',
'active' => '',
'languageId' => '',
        ]);
        GuideHelper::addEntity($validated);

        return to_route('guides', [
            'contact' => request('contactId')
        ]);
    }

    public function update(Guide $guide)
    {
        $validated = request()->validate([
            'name' => '',
'email' => '',
'mobile' => '',
'photoPath' => '',
'dob' => '',
'active' => '',
'languageId' => '',
        ]);
        GuideHelper::updateEntity($guide, $validated);

        return to_route('guides', [
            'contact' => $guide->contact_id
        ]);
    }
}
