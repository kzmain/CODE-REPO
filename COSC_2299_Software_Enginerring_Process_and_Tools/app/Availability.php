<?php

/*

The Availability class represents the availability of an employee for a
single day of the week, and is represented by the start time and end time.

*/

namespace App;

use App\Employee;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Validator;

class Availability extends Model
{
    protected $fillable = ['employee_id', 'day_of_week', 'start_time', 'end_time'];

    /* This is a validator for sanity checking and unit testing */
    public static function validator(array $data) {
        return Validator::make($data, [
            'start_time' => 'required|valid24hourtime',
            'end_time' => 'required|valid24hourtime|greaterthanintegerfield:start_time'
        ],
        [
            'valid24hourtime' => 'Not a valid time',
            'greaterthanintegerfield' => 'Must be after start time',
        ]);
    }

    /* Each availability belongs to an employee */
    public function employee() {
        return $this->belongsTo(Employee::class);
    }

    /* Return the day_of_week as text instead of a number */
    public function day_of_week_as_text() {
        if ($this->day_of_week == 1) {
            return 'Sunday';
        }
        if ($this->day_of_week == 2) {
            return 'Monday';
        }
        if ($this->day_of_week == 3) {
            return 'Tuesday';
        }
        if ($this->day_of_week == 4) {
            return 'Wednesday';
        }
        if ($this->day_of_week == 5) {
            return 'Thursday';
        }
        if ($this->day_of_week == 6) {
            return 'Friday';
        }
        if ($this->day_of_week == 7) {
            return 'Saturday';
        }
        
        return 'Invalid Day of Week';
    }

}
