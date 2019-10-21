<?php

/*

The Business class represents a business. It's a crazy world.

*/

namespace App;

use Illuminate\Database\Eloquent\Model;

class Business extends Model
{
    protected $fillable = ['name'];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'name' => 'required|max:255',

        ]);
      }

    /* Each user is associated with a business */
    public function users() {
        return $this->hasMany('App\User');
    }

    /* Each employee is associated with a business */
    public function employees() {
        return $this->hasMany('App\Employee');
    }
}
