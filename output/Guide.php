<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Guide extends Model
{
    const CREATED_AT = 'created_on';
    const UPDATED_AT = 'modified_on';

    protected $primaryKey = 'guide_id';

    protected $fillable = [
        'name',
'email',
'mobile',
'photo_path',
'active',
'language_id',
'contactId',
    ];
}
