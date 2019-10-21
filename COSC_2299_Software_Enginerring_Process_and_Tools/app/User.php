<?php

/*

The User class represents a customer, and is used for logging in and registering.

*/

namespace App;

use Illuminate\Notifications\Notifiable;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Support\Facades\Validator;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'name', 'address', 'city', 'state', 'postcode', 'phone', 'email', 'password',
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'name' => 'required|max:255|lettersandspacesonly',
            'email' => 'required|email|max:255|unique:users',
            'password' => 'required|min:6|confirmed|regex:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/',
            'address' => 'required|max:255',
            'city' => 'required|max:255|lettersandspacesonly',
            'state' => 'required|in:NSW,VIC,QLD,TAS,SA,NT,WA',
            'postcode' => 'required|digits:4',
            'phone' => 'required|digits:10|regex:/^0[23478][0-9]{8}$/'
        ],
        [
            'lettersandspacesonly' => 'Can only contain letters and spaces.'
        ]);
    }

    /*
        If this is empty, the user is a customer
        Otherwise, it specifies the admin of a business
    */
    public function business() {
        return $this->belongsTo('App\Business');
    }

}
