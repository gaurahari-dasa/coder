<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class SpecialPuja extends Model
{
    const CREATED_AT = 'created_on';
    const UPDATED_AT = 'modified_on';

    protected $primaryKey = 'special_puja_id';

    protected $fillable = [
        'puja_date',
'occasion_id',
'sevak_name',
'relationship_id',
'active',
'contact_id',
    ];
}
