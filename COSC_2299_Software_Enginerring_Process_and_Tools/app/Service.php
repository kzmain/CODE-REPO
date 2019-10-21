<?php

/*

The Service class represents a service that can be provided by an employee to a user.
Each service has a name and a duration in minutes.

*/

namespace App;

use App\Employee;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Validator;

class Service extends Model
{
    protected $fillable = ['name', 'duration_in_minutes'];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'name' => 'required|max:255|unique:services',
            'duration_in_minutes' => 'required|integer|min:1|max:1440',

        ]);
      }
}
